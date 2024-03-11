from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from area.models import Area
from order.models import Order

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='table_account')
    is_active = models.BooleanField(default=True)
    order =models.ForeignKey(Order, on_delete=models.PROTECT,null=True, blank=True, related_name='table_order')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='table_account')
    top = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    left = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='table_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='table_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='table_updated_by')