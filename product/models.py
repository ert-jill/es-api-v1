from django.db import models
from django.contrib.auth.models import User
from account.models import Account
# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stocks = models.PositiveIntegerField()
    is_group_parent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='product_account')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='product_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='product_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='product_updated_by')

    @property
    def product_items(self):
        return GroupProduct.objects.filter(parent_product=self)

class GroupProduct(models.Model):
    parent_product =  models.ForeignKey(Product, on_delete=models.PROTECT, related_name='group_product_parent_product')
    product =  models.ForeignKey(Product, on_delete=models.PROTECT, related_name='group_product_product')
    quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='group_product_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='group_product_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='group_product_updated_by')
