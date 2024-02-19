from django.db import models
from django.contrib.auth.models import User
from account.models import Account
# Create your models here.

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255, null=True, blank=True,)
    description = models.TextField( null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='payment_method_account')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_method_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='payment_method_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='dpayment_method_updated_by')
