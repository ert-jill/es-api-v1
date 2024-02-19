from rest_framework import serializers

from user_type.models import UserType

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ["id", "name", "description", "is_active"]