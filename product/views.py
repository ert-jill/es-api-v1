from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from user.tokens import get_user_from_token
from .serializers import ProductSerializer
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