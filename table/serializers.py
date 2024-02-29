# serializers.py

from rest_framework import serializers
from area.models import Area

from area.serializers import AreaSerializer
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    area = serializers.PrimaryKeyRelatedField(queryset= Area.objects.all(), write_only=True)
    class Meta:
        model = Table
        fields =  ('id', 'name', 'code', 'area', 'is_active')
        read_only_fields =("id","is_active",)

class TableReadSerializer(TableSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Table
        fields =  ('id', 'name', 'code', 'area', 'is_active')
        read_only_fields =("id","is_active",)