from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Account, UserAccount
from django.db import transaction

from account.serializers import AccountSerializer
from user.models import UserUserAccount, UserUserType
from user_type.models import UserType
from user_type.serializers import UserTypeSerializer


class UserUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUserAccount
        fields = ["user", "account", "status"]
        read_only_fields = ("user", "status")


class UserUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUserType
        fields = ["user", "user_type", "status"]
        read_only_fields = ("user", "status")


class UserSerializer(serializers.ModelSerializer):
    user_user_type = serializers.SerializerMethodField()
    user_user_account = serializers.SerializerMethodField()
    user_type = serializers.PrimaryKeyRelatedField(queryset= UserType.objects.all(),write_only=True)
    user_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(),write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "user_user_type",
            "user_user_account",
            "user_type",
            "user_account",
        ]
        

    def get_user_user_type(self, obj):
        # Retrieve the related UserType object and serialize it
        user_type_obj = UserUserType.objects.filter(user=obj).first()
        if (
            user_type_obj is not None
        ):  # Assuming `usertype` is the related name of the user type field in the User model
            user_type_data = UserUserTypeSerializer(user_type_obj).data
            return user_type_data
        else:
            return None

    def get_user_user_account(self, obj):
        # Retrieve the related UserType object and serialize it
        user_account_obj = UserUserAccount.objects.filter(
            user=obj
        ).first()  # Assuming `usertype` is the related name of the user type field in the User model
        if user_account_obj is not None:
            user_account_data = UserUserAccountSerializer(user_account_obj).data
            return user_account_data
        else:
            return None
    def create(self, validated_data):
        user_type = validated_data.pop("user_type")
        user_account = validated_data.pop("user_account")
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            UserUserAccount.objects.create(user=user, account=user_account)
            UserUserType.objects.create(user=user, user_type=user_type)

        return user


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

    def get_user_type(self, obj):
        user_type_obj = UserUserType.objects.filter(user=obj).first()
        if user_type_obj is not None:
            serializer = UserTypeSerializer(user_type_obj.user_type)
            return serializer.data
        return ""

    def get_account(self, obj):
        user_account_instance = obj.useraccount_set.order_by("-dateAdded").first()
        if user_account_instance is not None:
            serializer = AccountSerializer(user_account_instance.account)
            return serializer.data
        return ""

    def create(self, validated_data):
        user_account_data = validated_data.pop("user_account")
        user_type_data = validated_data.pop("user_user_type")
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            UserAccount.objects.create(user=user, **user_account_data)
            UserUserType.objects.create(user=user, **user_type_data)

        return user


# class UserUserTypeSerializer(serializers.ModelSerializer):
#     user = AccountUserSerializer()
#     user_type = UserTypeSerializer()

#     class Meta:
#         model = UserUserType
#         fields = ["user", "user_type", "status"]
#         depth = 1
#         ref_name = "UserUserType"


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
