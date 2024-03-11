from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from user.models import UserUserAccount
from user.tokens import get_user_from_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from .models import Order, OrderItem
from .serializers import AddOrderItemQuantitySerializer, AddOrderItemSerializer, OrderItemSerializer, OrderSerializers,VoidOrderItemSerializer  # Make sure to replace this with your actual serializer
from rest_framework.response import Response
from drf_yasg import openapi

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: OrderSerializers},
        operation_description='Get orders',
        tags=["Order"]
    )
    # @permission_classes([IsAuthenticated])
    def list(self, request):
        user = get_user_from_token(request.auth)
        # get user's account
        user_account_instance = UserUserAccount.objects.get(pk=user.id)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        queryset = Order.objects.filter(account = account_instance)
        serializer = OrderSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderSerializers,
        responses={status.HTTP_201_CREATED: OrderSerializers},
        operation_description='Create a new order',
        tags=["Order"]
    )
    # @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_account_instance = UserUserAccount.objects.get(user=user)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise user_account_instance.ValidationError({"account": "Account not found"})
        # Extract order data from the request data
        order_data = request.data.copy()
        # initialized serializer
        order_serializer = OrderSerializers(data=order_data)
        # check if order data is valid
        if order_serializer.is_valid():
            # save order
            order_serializer.save(created_by_user=user,account = account_instance)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        responses={200: OrderSerializers()},
        operation_summary="Retrieve a order",
        tags=["Order"],
    )
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=AddOrderItemSerializer,
        responses={status.HTTP_201_CREATED: AddOrderItemSerializer},
        operation_description='Create a new order item',
        tags=["Order"]
    )
    # @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def add_order_item(self, request, *args, **kwargs):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_account_instance = UserUserAccount.objects.get(user=user)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise user_account_instance.ValidationError({"account": "Account not found"})
        
        item_data = request.data.copy()

        item_serializer = AddOrderItemSerializer(data=item_data)

        if item_serializer.is_valid():
            item_serializer.save(created_by_user=user)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        request_body=VoidOrderItemSerializer,
        responses={status.HTTP_200_OK: VoidOrderItemSerializer},
        operation_description='Item void successfully',
        tags=["Order"]
    )
    # @permission_classes([IsAuthenticated])
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
        
    @swagger_auto_schema(
    responses={status.HTTP_200_OK: OrderItemSerializer(many=True)},
    operation_description='Get order item',
    tags=["Order"],
    manual_parameters=[
        openapi.Parameter(
            'order',
            openapi.IN_QUERY,
            description="order id",
            type=openapi.TYPE_STRING,
            required=False
        ),
       
    ]
    )
    @action(detail=False, methods=["get"])
    def get_order_item(self, request):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        order = request.query_params.get('order')
        # Extract order data from the request data
        item_data = OrderItem.objects.filter(order_id = order)
        # initialized serializer
        item_serializer = OrderItemSerializer(item_data, many=True)
        return Response(item_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=AddOrderItemQuantitySerializer, responses={200: AddOrderItemQuantitySerializer()}, tags=["Order"], manual_parameters=[
        openapi.Parameter(
            'order_item',
            openapi.IN_QUERY,
            description="order item id",
            type=openapi.TYPE_STRING,
            required=False
        ),
       
    ],)
    @action(detail=False, methods=["put"])
    def set_order_item_quantity(self, request):
        order_item_id = request.query_params.get('order_item')
        order_item = OrderItem.objects.get(pk=order_item_id)
        serializer = AddOrderItemQuantitySerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by_user = request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        