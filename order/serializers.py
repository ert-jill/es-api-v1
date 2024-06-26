from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer
from user.serializers import UserSerializer
from user.tokens import User
from .models import Order, OrderItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "order",
            "product",
            "quantity",
            "product_total",
            "product_discount",
            "is_void",
        )

    def get_product(self, obj):
        # Assuming 'product' is the related field in OrderItem
        product_instance = obj.get("product")
        return ProductSerializer(product_instance).data


class AddOrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=True
    )
    sku = serializers.CharField(write_only=True, required=True)
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "sku",
            "order",
            "product",
            "quantity",
            "product_total",
            "product_discount",
            "is_void",
        )
        read_only_fields = (
            "product_total",
            "product_discount",
            "product",
            "is_void",
        )
        write_only_fields = (
            "sku",
            "order",
            "quantity",
        )

        depth = 1

    def get_product(self, obj):
        # Assuming 'product' is the related field in OrderItem
        product_instance = obj.get("product")
        return ProductSerializer(product_instance).data

    def add_order_item(self, validated_data):
        # get user
        user = self.context.get("user")
        user_account_instance = user.useraccount_set.order_by("-dateAdded").first()
        # Extract the product ID from validated_data
        sku = validated_data.pop("sku", None)
        order = validated_data.get("order")

        # Assuming your model has a 'product' field that is a ForeignKey to the Product model
        product = Product.objects.get(sku=sku)

        # order = order_id
        user_account = user_account_instance.account
        orders_account = order.account
        product_account = product.account
        if (
            user_account_instance.account != product_account
            and user_account != orders_account
        ):
            raise serializers.ValidationError(
                "User account and product account or order account do not match."
            )

        # Calculate total price based on quantity and product price
        validated_data["product"] = product
        # validated_data["order"] = order
        quantity = validated_data.get("quantity", 0)
        product_price = product.price
        total_price = quantity * product_price

        # Populate other fields based on the product
        validated_data["product_name"] = product.name
        validated_data["product_price"] = product.price
        validated_data["product_description"] = product.description
        validated_data["product_total"] = total_price

        # Create the OrderItem instance
        # use transaction for data integrity
        with transaction.atomic():
            order_item_found = OrderItem.objects.filter(
                order=validated_data.get("order"), product=validated_data.get("product")
            )
            if order_item_found.exists():
                order_item = order_item_found[0]  # get the order item found

                order.total -= (
                    order_item.product_total
                )  # update the order total remove the old order item product total

                order_item.quantity = quantity
                order_item.product_total = total_price
                order_item.updated_by_user = user
                order_item.save()

            else:
                order_item = OrderItem.objects.create(
                    created_by_user=user, **validated_data
                )

            order.total += total_price
            order.updated_by_user = user
            order.save()

        return order_item


class VoidOrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=True
    )
    sku = serializers.CharField(write_only=True, required=True)
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "sku",
            "order",
            "product",
            "quantity",
            "product_total",
            "product_discount",
            "is_void",
            "quantity",
        )
        read_only_fields = (
            "product_total",
            "product_discount",
            "product",
            "quantity",
            "is_void",
        )
        write_only_fields = (
            "sku",
            "order",
        )

        depth = 1

    def get_product(self, obj):
        # Assuming 'product' is the related field in OrderItem
        product_instance = obj.get("product")
        return ProductSerializer(product_instance).data

    def void_order_item(self, validated_data):
        # get user
        user = self.context.get("user")
        user_account_instance = user.useraccount_set.order_by("-dateAdded").first()
        # Extract the product ID from validated_data
        sku = validated_data.pop("sku", None)
        order = validated_data.get("order")

        # Assuming your model has a 'product' field that is a ForeignKey to the Product model
        product = Product.objects.get(sku=sku)

        # order = order_id
        user_account = user_account_instance.account
        orders_account = order.account
        product_account = product.account
        if (
            user_account_instance.account != product_account
            and user_account != orders_account
        ):
            raise serializers.ValidationError(
                "User account and product account or order account do not match."
            )
        
         # Calculate total price based on quantity and product price
        validated_data["product"] = product
        product_price = product.price
        total_price = 0

        # Populate other fields based on the product
        validated_data["product_name"] = product.name
        validated_data["product_price"] = product_price
        validated_data["product_description"] = product.description
        validated_data["product_total"] = total_price


        # use transaction for data integrity
        with transaction.atomic():
            order_item_found = OrderItem.objects.filter(
                order=order, product=product
            )
            if order_item_found.exists():
                order_item = order_item_found[0]  # get the order item found
                order.total -= (
                    order_item.product_total
                )  # minus the order product total ammount to the order total
                order_item.quantity = 0
                order_item.product_total = 0
                order_item.is_void = True
                order_item.is_void_by_user = user
                order_item.save()

            else:
                raise serializers.ValidationError("Order Item not found")

            order.updated_by_user = user
            order.save()

        return order_item


class UserCreatedBySeriaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["account"]
        ref_name = "CreatedByUser"


class CreateOrderSerializer(serializers.ModelSerializer):
    # created_by_user = UserSerializer(write_only=True)
    # order_items = OrderItemSerializer(many=True, required=False, allow_empty=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    # def _get_children(self, obj):
    #     serializer = OrderItemSerializer(obj.child_list(), many=True)
    #     return serializer.data
    class Meta:
        model = Order
        fields = (
            "id",
            "account",
            "total",
            "total_discount",
            "order_items",
            "customer",
            "is_void",
            # "created_date",
            # "updated_date",
            # "updated_by_user",
            "payment_method",
            "payment_status",
            "shipping_address",
            "shipping_status",
            "tracking_info",
            "order_status",
        )
        read_only_fields = (
            "id",
            "account",
            "total",
            "total_discount",
            "payment_reference_no",
            "is_void",
            # "created_date",
            # "updated_date",
            # "updated_by_user",
            "payment_status",
            "shipping_status",
            "tracking_info",
            "order_status",
        )

    def create(self, validated_data):
        # get user
        user = self.context.get("user")
        # get user's account
        user_account_instance = user.useraccount_set.order_by("-dateAdded").first()
        # check if user's has account tagged
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializers.ValidationError({"account": "Account not found"})

        # get order items
        # order_items_data = validated_data.pop("order_items", [])

        # use transaction for data integrity
        # with transaction.atomic():

        order_instance = Order.objects.create(
            created_by_user=user, account=account_instance, **validated_data
        )

        # Check if order_items_data is present before attempting to create order items
        # if order_items_data is not None and order_items_data:
        #     order_items_serializer = OrderItemSerializer(
        #         data=order_items_data, many=True
        #     )
        #     if order_items_serializer.is_valid():
        #         ordered_items = order_items_serializer.save(order=order_instance)
        #         # Calculate the sum of product_total values from ordered_items
        #         total_product_total = sum(item.product_total for item in ordered_items)

        #         # Update the order_instance with the total_product_total
        #         order_instance.total = total_product_total
        #         order_instance.save()
        #     else:
        #         # Rollback the transaction if order items are not valid
        #         raise serializers.ValidationError(order_items_serializer.errors)
        # Serialize the order instance along with its order items
        return order_instance
