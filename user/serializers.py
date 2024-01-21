from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import UserAccount
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields  =['id','username','password','email','firstname','lastame']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ForceChangePassSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['account']
        ref_name = 'UserAccount'

class AccountUserSerializer(serializers.ModelSerializer):
    user_account = AccountSerializer(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name','last_name','user_account','email']

    def create(self, validated_data):
        user_account_data = validated_data.pop('user_account')
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            UserAccount.objects.create(user=user, **user_account_data)
        return user

