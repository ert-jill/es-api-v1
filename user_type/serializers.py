from rest_framework import serializers

from user_type.models import UserType

class UserTypeSerializer(serializers.ModelSerializer):
    id = serializers.CharField()  # Ensure id is read-only
    class Meta:
        model = UserType
        fields = ["id", "name", "description", "is_active"]
        read_only_fields = ("name", "description", "is_active")
        write_only_fields=("id",)
        extra_kwargs = {
            "id": {"write_only": True},  # Mark id as write-only
        }