from rest_framework import serializers
from .models import Account


# default account serializer
class AccountSerializer(serializers.ModelSerializer):
    # owner = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "ownerName",
            "email",
            "contactNumber",
            "address",
            "status",
        ]
        read_only_fields = (
            "name",
            "ownerName",
            "email",
            "contactNumber",
            "address",
            "status",
        )
        write_only_fields = ("id")
        ref_name = "Account"

    # auto detect the owner variable where its result to be stored
    # def get_owner(self, obj):
    #     return obj.ownerName
