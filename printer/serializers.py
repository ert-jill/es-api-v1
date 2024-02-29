from rest_framework import serializers
from .models import Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = [
            "id",
            "name",
            "description",
            "connection",
            "is_active",
        ]
        read_only_fields =("id",)
