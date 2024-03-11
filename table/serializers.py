# serializers.py

from rest_framework import serializers
from area.models import Area

from area.serializers import AreaSerializer
import transaction
from .models import Table


class TableSerializer(serializers.ModelSerializer):
    area = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(), write_only=True
    )

    class Meta:
        model = Table
        fields = ("id", "name", "code", "order", "area", "is_active", "top", "left")
        read_only_fields = (
            "id",
            "is_active",
        )



class TableReadSerializer(TableSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Table
        fields = ("id", "name", "code", "area", "order", "is_active", "top", "left")
        read_only_fields = (
            "id",
            "is_active",
        )
