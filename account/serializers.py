from rest_framework import serializers
from .models import Account, AccountType


# default account serializer
class AccountWriteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    account_type = serializers.PrimaryKeyRelatedField(queryset= AccountType.objects.all())
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "ownerName",
            "email",
            "contactNumber",
            "account_type",
            "address",
            "status",
        ]
        depth=1
        read_only_fields = (
            "id",
            "status",
        )
        ref_name = "WriteAccount"
class AccountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "ownerName",
            "email",
            "contactNumber",
            "account_type",
            "address",
            "status",
        ]
        depth=1
        read_only_fields = (
            "id",
            "status",
        )
        ref_name = "Account"

    # auto detect the owner variable where its result to be stored
    # def get_owner(self, obj):
    #     return obj.ownerName

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name', 'code']
