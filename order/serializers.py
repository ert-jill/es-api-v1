from rest_framework import serializers
from product.models import Product
from product.serializers import ProductSerializer
from user.tokens import User
from .models import Order, OrderItem
from django.db import transaction

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ("account","created_by_user")
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='sku',
        required=True
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_instance = instance.product  # Assuming product is a ForeignKey field in Order model
        product_serializer = ProductSerializer(product_instance)
        representation['product'] = product_serializer.data
        return representation
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "quantity",
            "is_void",
            "is_placed",
        )
        read_only_fields = ("id",)
    
    def create(self, validated_data):
        product = validated_data.pop("product")
        return OrderItem.objects.create( product = product, product_name=product.name, product_price = product.price, product_description = product.description, **validated_data)


class AddOrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=True
    )
    sku = serializers.CharField(
        write_only=True,
        required=True,
    )
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "quantity",
            "product_total",
            "product_discount",
            "is_void",
            "sku",
        )
        read_only_fields = ("id","product_total", "product_discount", "is_void", "ptroduct")
        depth = 1

    def get_product(self, obj):

        # Assuming 'product' is the related field in OrderItem

        product_instance = obj.product

        return ProductSerializer(product_instance).data

    def create(self, validated_data):
        # user = self.context['request'].user  # Accessing user data from context
        # validated_data['created_by'] = user
        sku = validated_data.pop("sku")
        # Calculate total price based on quantity and product price
        product = Product.objects.get(sku=sku)
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

        order = validated_data.get("order")
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
                order_item.updated_by_user = validated_data["created_by_user"]
                order_item.save()

            else:
                order_item = OrderItem.objects.create(**validated_data)

            order.total += total_price
            order.updated_by_user = order_item.created_by_user
            order.save()

        return order_item


class AddOrderItemQuantitySerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField( read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "quantity",
            "product_total",
            "product_discount",
            "is_void",
        )
        read_only_fields = (
            "id",
            "order",
            "product",
            "product_total",
            "product_discount",
            "is_void",
        )
        depth=1
    def get_product(self, obj):
        # Assuming 'product' is the related field in OrderItem
        product_instance = obj.product
        return ProductSerializer(product_instance).data
    
    def update(self, instance, validated_data):
        product = instance.product
        quantity = validated_data.get("quantity")
        product_price = product.price
        total_price = quantity * product_price
    def get(self, instance):
        # Custom logic to retrieve data from the instance or serializer's context
        # You can access instance data or serializer context using self.instance and self.context
        return self.instance.some_method()

        order = instance.order
        with transaction.atomic():

            order.total -= (
                instance.product_total
            )  # update the order total remove the old order item product total
            instance.quantity = quantity
            instance.product_total = total_price
            instance.save()

            order.total += total_price
            order.updated_by_user = instance.updated_by_user
            order.save()
            return instance


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
            order_item_found = OrderItem.objects.filter(order=order, product=product)
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

    order_items = OrderItemSerializer(many=True, read_only=True)

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
            "payment_status",
            "shipping_address",
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


# class OrderSerializers(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = [
#             "id",
#             "is_void",
#             "total",
#             "total_discount",
#             "total_vat",
#             "order_items",
#             "customer",
#             "order_status",
#         ]
#         read_only_fields = (
#             "id",
#             "is_void",
#             "total",
#             "total_discount",
#             "order_items",
#             "order_status",
#         )

#     def validate_tables(self, value):
#         """
#         Validate that the tables is vacant for dine-in orders.
#         """
#         if value is not None:
#             t = value.split(",")
#             to_update_table = Table.objects.filter(id__in=t, order=None)
#             if len(t) != len(to_update_table):
#                 raise serializers.ValidationError("Table not available")
#         return value

#     def create(self, validated_data):

#         with transaction.atomic():
#             order = Order.objects.create(**validated_data)
#             tables = validated_data.get("tables")
#             if tables is not None:
#                 t = tables.split(",")
#                 updated_records = Table.objects.filter(id__in=t, order=None).update(
#                     order=order
#                 )
#                 if len(t) != updated_records:
#                     raise Exception("Table is not available, but pass the validation")
#         return order
