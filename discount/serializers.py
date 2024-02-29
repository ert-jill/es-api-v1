from rest_framework import serializers

from product.models import Product
from .models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    discounted_product =  serializers.PrimaryKeyRelatedField(queryset= Product.objects.all(), required = False)
    expiry_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', required=False) #YYYY-MM-DDTHH:MM:SS
    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "code",
            "description",
            "amount",
            "amount_type",
            "is_active",
            "expiry_date",
            "discounted_product",
            "account",
        ]
        read_only_fields = ("id","account","is_active",)
