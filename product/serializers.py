from rest_framework import serializers
from .models import GroupProduct, Product
from django.db import transaction

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'sku',
            'name',
            'description',
            'price',
            'stocks',
            'account',
        ]
        ref_name = 'Product' 

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

class GroupProductItemSerializer(serializers.ModelSerializer):

    sku = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = GroupProduct
        fields = [
            'parent_product',
            'product',
            'sku',
            'quantity',
        ]
        read_only_fields = (
            'parent_product',
            'product',
        )
        ref_name = 'GroupProductItem'

    def create(self, validated_data):
        sku = validated_data.pop("sku", None)
        product = Product.objects.get(sku=sku)
        validated_data["product"] = product
        return super().create(validated_data)
    
    def validate(self, data):
        # Perform your custom validation checks here
        sku = data.get('sku')
        product = Product.objects.get(sku=sku)
        if data.quantity<=0 :
            raise serializers.ValidationError("Please ensure that each group product item has a minimum quantity of one or more.")
        if product is not None:
            # Check if the field value meets certain criteria
            if product.is_group_parent :
                raise serializers.ValidationError("It is not possible to include a parent group product as a part of another group product.")
        # Always return the validated data
        return data

class GroupProductSerializer(serializers.ModelSerializer):
    product_items = GroupProductItemSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'sku',
            'name',
            'description',
            'price',
            'stocks',
            'product_items',
        ]
        ref_name = 'GroupProduct'
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

        # get product items
        product_items_data = validated_data.pop("product_items", [])

        # use transaction for data integrity
        with transaction.atomic():

            product_instance = Product.objects.create(
                created_by_user=user, account=account_instance,is_group_parent=True, **validated_data
            )

        # Check if order_items_data is present before attempting to create order items
            if product_items_data is not None and product_items_data:
                    
                product_items_serializer = GroupProductItemSerializer(
                    data=product_items_data, many=True
                )
                if product_items_serializer.is_valid():
                    product_items_serializer.save(parent_product=product_instance, created_by_user=user)
                else:
                    # Rollback the transaction if order items are not valid
                    raise serializers.ValidationError(product_items_serializer.errors)
        # Serialize the order instance along with its order items
        return product_instance
        
