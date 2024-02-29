from django.db import models
from django.contrib.auth.models import User
from account.models import Account

# Create your models here.
class Printer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField()
    connection = models.CharField()
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='printer_account')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='printer_created_by')
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='printer_deleted_by')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='printer_updated_by')