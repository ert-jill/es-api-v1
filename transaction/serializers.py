from rest_framework import serializers
from .models import Transaction

class TransactionSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','table','customer','total_amount','total_vat','total_discount','transaction_status']
        read_only_fields = ('id','total_amount','total_vat','total_discount','transaction_status')
