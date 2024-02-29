from rest_framework import serializers

from user.models import UserUserAccount
from .models import GroupProduct, Product
from django.db import transaction


class GroupProductItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    sku = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = GroupProduct
        fields = [
            "parent_product",
            "product",
            "sku",
            "quantity",
            "price",
        ]
        read_only_fields = (
            "parent_product",
            "product",
        )
        ref_name = "GroupProductItem"

    def create(self, validated_data):
        sku = validated_data.pop("sku", None)
        product = Product.objects.get(sku=sku)
        validated_data["product"] = product
        return super().create(validated_data)

    def validate(self, data):
        # Perform your custom validation checks here
        sku = data.get("sku")
        product = Product.objects.get(sku=sku)
        if data.get("quantity") <= 0:
            raise serializers.ValidationError(
                "Please ensure that each group product item has a minimum quantity of one or more."
            )
        if product is not None:
            # Check if the field value meets certain criteria
            if product.is_group_parent:
                raise serializers.ValidationError(
                    "It is not possible to include a parent group product as a part of another group product."
                )
        # Always return the validated data
        return data


class ProductSerializer(serializers.ModelSerializer):
    product_items = GroupProductItemSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "stocks",
            "product_items",
        ]
        read_only_fields = ("id",)
        ref_name = "GroupProduct"

    def create(self, validated_data):
        # get user
        user = self.context.get("user")
        # get user's account
        user_account_instance = UserUserAccount.objects.get(user=user)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializers.ValidationError({"account": "Account not found"})

        # get product items
        product_items_data = validated_data.pop("product_items", [])

        # use transaction for data integrity
        with transaction.atomic():

            # Check if order_items_data is present before attempting to create order items
            if product_items_data is not None and product_items_data:
                product_instance = Product.objects.create(created_by_user_id=user.id, account=account_instance,
                    is_group_parent=True,
                    **validated_data
                )
                product_items_serializer = GroupProductItemSerializer(
                    data=product_items_data, many=True
                )
                if product_items_serializer.is_valid():
                    product_items_serializer.save(created_by_user_id=user.id,
                        parent_product=product_instance
                    )
                else:
                    # Rollback the transaction if order items are not valid
                    raise serializers.ValidationError(product_items_serializer.errors)
            else :
                product_instance = Product.objects.create(created_by_user_id=user.id, account=account_instance,
                    **validated_data
                )
        # Serialize the order instance along with its order items
        return product_instance
