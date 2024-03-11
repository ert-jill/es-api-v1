from django.db import models
from django.contrib.auth.models import User

from account.models import Account

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Void', 'Void'),
    )
    table = models.CharField(max_length=100,null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_vat = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    customer = models.CharField(max_length=255,null=True, blank=True)  # You may want to replace this with a ForeignKey to another model representing customers
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_transactions')
    created_date = models.DateTimeField(auto_now_add=True)
    void_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='voided_transactions')
    void_date = models.DateTimeField(null=True, blank=True)
    transaction_status = models.CharField(max_length=100, choices=TRANSACTION_STATUS_CHOICES,default = 'Pending')

