from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from user.tokens import get_user_from_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from .models import Order
from .serializers import AddOrderItemSerializer,VoidOrderItemSerializer, CreateOrderSerializer  # Make sure to replace this with your actual serializer
from rest_framework.response import Response

class OrderViewSet(viewsets.ViewSet):
    # queryset = Order.objects.all()
    # serializer_class = CreateOrderSerializer  # Replace with your actual serializer class
    # permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

    # def get_serializer_class(self):
    #     # Use different serializers for input and output
    #     if self.action in ['create']:
    #         return CreateOrderSerializer
    #     return CreateOrderSerializer

    @swagger_auto_schema(
        request_body=CreateOrderSerializer,
        responses={status.HTTP_201_CREATED: CreateOrderSerializer},
        operation_description='Create a new order',
        tags=["Order"]
    )
    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Extract order data from the request data
        order_data = request.data.copy()
        # initialized serializer
        order_serializer = CreateOrderSerializer(data=order_data, context={'user': user})
        # check if order data is valid
        if order_serializer.is_valid():
            # save order
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=AddOrderItemSerializer,
        responses={status.HTTP_201_CREATED: AddOrderItemSerializer},
        operation_description='Create a new order item',
        tags=["Order"]
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def add_order_item(self, request, *args, **kwargs):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Extract order data from the request data
        item_data = request.data.copy()
        # initialized serializer
        item_serializer = AddOrderItemSerializer(data=item_data, context={'user': user })
        # check if order data is valid
        if item_serializer.is_valid():
            # save order
            item_serializer.add_order_item(item_serializer.validated_data)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        request_body=VoidOrderItemSerializer,
        responses={status.HTTP_200_OK: VoidOrderItemSerializer},
        operation_description='Item void successfully',
        tags=["Order"]
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["put"])
    def void_order_item(self, request, *args, **kwargs):
        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Extract order data from the request data
        item_data = request.data.copy()
        # initialized serializer
        item_serializer = VoidOrderItemSerializer(data=item_data, context={'user': user})
        # check if order data is valid
        if item_serializer.is_valid():
            # save order
            item_serializer.void_order_item(item_serializer.validated_data)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def update(self, request, *args, **kwargs):
    #     #get user
    #     user = get_user_from_token(request.auth)
    #     #check if their is a user
    #     if user is None:
    #         return Response(
    #             {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
    #         )
        
    #     # Extract order data from the request data
    #     order_data = request.data.copy()

    #     order_serializer = OrderSerializer(data=order_data, context={'user': user})

    #     if order_serializer.is_valid():
            
    #         order_serializer.save()
    #         return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)