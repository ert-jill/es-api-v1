from rest_framework import serializers
from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"
        read_only_fields = (
            "account",
            "is_active",
            "created_date",
            "deleted_date",
            "updated_date",
            "account",
            "created_by_user",
            "deleted_by_user",
            "updated_by_user",
        )
