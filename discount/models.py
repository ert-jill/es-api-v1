from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from order.models import Order, OrderItem
from product.models import Product
# Create your models here.

class Discount(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    discounted_product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='discount_product')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_type = models.CharField(max_length=25) #amount or percentage
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='discount_account')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='discount_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='discount_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='discount_updated_by')

class OrderDiscount(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    order_item = models.ForeignKey(OrderItem, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_discount_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='order_discount_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='order_discount_updated_by')
    
    class Meta:
        unique_together = ('order', 'order_item', 'discount')