from rest_framework import serializers

from user_type.models import UserType

class UserTypeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure id is read-only
    class Meta:
        model = UserType
        fields = ["id", "name", "description", "is_active"]
        read_only_fields = ("id","is_active")