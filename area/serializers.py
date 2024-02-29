
from rest_framework import serializers
from .models import Area

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'code', 'is_active')
        read_only_fields = ("id",'is_active',)