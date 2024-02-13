from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from user.tokens import get_user_from_token
from .serializers import GroupProductSerializer, ProductSerializer
# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={status.HTTP_201_CREATED: 'Product created successfully'},
        operation_description='Create a new product',
        tags=["Product"]
    )

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by_user_id=user.id)  # Assuming you have user authentication
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @swagger_auto_schema(
        request_body=GroupProductSerializer,
        responses={status.HTTP_201_CREATED: GroupProductSerializer},
        operation_description='Create a new group product',
        tags=["Product"]
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def add_group_product(self, request, *args, **kwargs):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Extract order data from the request data
        data = request.data.copy()
        # initialized serializer
        serializer = GroupProductSerializer(data=data, context = {'user': user })
        # check if order data is valid
        if serializer.is_valid():
            # save order
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)