from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderSerializer
from user.models import UserUserAccount


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all orders",
        tags=["Order"],
        manual_parameters=[
            openapi.Parameter(
                "by",
                openapi.IN_QUERY,
                description="get order by",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: OrderSerializer(many=True)},
    )
    def list(self, request):
        """
        List all orders.
        """
        user_account_instance = UserUserAccount.objects.get(user=request.user)

        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        by = request.query_params.get("by")
        if by is not None:
            if by == "table":
                queryset = Order.objects.filter(
                    account=account_instance, table__isnull=False
                )
            elif by == "to go":
                queryset = Order.objects.filter(
                    account=account_instance, table__isnull=True
                )
            else:
                queryset = Order.objects.filter(account=account_instance)
        else:
            queryset = Order.objects.filter(account=account_instance)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve an order by ID",
        tags=["Order"],
        responses={200: OrderSerializer()},
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve an order by ID.
        """
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new order",
        tags=["Order"],
        request_body=OrderSerializer,
        responses={201: OrderSerializer()},
    )
    def create(self, request):
        """
        Create a new order.
        """
        user_account_instance = UserUserAccount.objects.get(user=request.user)

        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user=request.user, account=account_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update an existing order",
        tags=["Order"],
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def update(self, request, pk=None):
        """
        Update an existing order.
        """
        order = get_object_or_404(Order.objects.all(), pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete an order by ID",
        tags=["Order"],
        responses={204: "No Content"},
    )
    def destroy(self, request, pk=None):
        """
        Delete an order by ID.
        """
        order = get_object_or_404(Order.objects.all(), pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Create a new order item",
        tags=["Order"],
        request_body=OrderItemSerializer,
        responses={201: OrderItemSerializer()},
    )
    @action(detail=False, methods=["post"])
    def order_item_create(self, request):
        """
        Create a new order.
        """
        # user_account_instance = UserUserAccount.objects.get(user=request.user)

        # if user_account_instance:
        #     # get assigned account
        #     account_instance = user_account_instance.account
        # else:
        #     # Handle the case where no UserAccount is found for the user
        #     raise serializer.ValidationError({"account": "Account not found"})

        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["put"],
        operation_summary="Update Order Item",
        operation_description="Update an order item by its primary key.",
        request_body=OrderItemSerializer,
        responses={200: OrderItemSerializer(), 400: "Error response description"},
        tags=["Order"],
    )
    @action(detail=False, methods=["put"], url_path=r"order_item_update/(?P<pk>[^/.]+)")
    def order_item_update(self, request, pk=None):
        print(pk)
        """
        Update new order.
        """
        model = OrderItem.objects.get(pk=pk)
        serializer = OrderItemSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by_user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get Order Order Items",
        operation_description="Get an order order items by its primary key.",
        responses={200: OrderItemSerializer(many=True)},
        tags=["Order"],
    )
    @action(
        detail=False, methods=["get"], url_path=r"order_item_update/(?P<order>[^/.]+)"
    )
    def order_item_get(self, request, order=None):
        print(order)
        """
            Update new order.
        """
        model = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
