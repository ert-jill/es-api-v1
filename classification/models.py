from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from product.models import Product
# Create your models here.

class Classification(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='parent_classification', null=True, blank=True)
    depth = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='classification_account')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='classification_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='classification_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='classification_updated_by')

class ProductClassification(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='product_classification_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='product_classification_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='product_classification_updated_by')
    
    class Meta:
        unique_together = ('product', 'classification')