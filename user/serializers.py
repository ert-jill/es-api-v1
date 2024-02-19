from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Account, UserAccount
from django.db import transaction

from account.serializers import AccountSerializer
from user.models import UserUserType
from user_type.serializers import UserTypeSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ForceChangePassSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["account"]
        ref_name = "UserAccount"

class UserTagUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUserType
        fields = ["user_type"]
        ref_name = "UserTagUserType"


class AccountUserSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(write_only=True)
    user_user_type = UserTagUserTypeSerializer(write_only=True)
    account = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "user_account",
            "user_user_type",
            "email",
            "account",
            "user_type",
        ]
        
    def get_user_type(self,obj):
        user_type_obj = UserUserType.objects.get(user=obj)
        serializer= UserTypeSerializer(user_type_obj.user_type)
        return serializer.data
    
    def get_account(self,obj):
        user_account_instance = obj.useraccount_set.order_by("-dateAdded").first()
        serializer = AccountSerializer(user_account_instance.account)
        return serializer.data
    

    def create(self, validated_data):
        user_account_data = validated_data.pop("user_account")
        user_type_data = validated_data.pop("user_type")
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            UserAccount.objects.create(user=user, **user_account_data)
            UserUserType.objects.create(user=user, **user_type_data)

        return user

class UserUserTypeSerializer(serializers.ModelSerializer):
    user = AccountUserSerializer()
    user_type = UserTypeSerializer()
    class Meta:
        model = UserUserType
        fields = ["user", "user_type", "status"]
        depth =1
        ref_name = "UserUserType"

class UserAccountSerializer1(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = ["account"]
        depth = 1
        ref_name = "UserAccount"

    def get_account(self, obj):
        account_instance = obj.get("account")
        return AccountSerializer(account_instance).data
