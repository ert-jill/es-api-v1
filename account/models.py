from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AccountType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=120)
    code = models.CharField(unique=True, max_length=120)

class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=120)
    ownerName = models.CharField(max_length=50)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='account_type')
    email = models.CharField(max_length=50)
    contactNumber = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='account_created_by')
    updatedDate = models.DateTimeField(null=True)
    deletedDate = models.DateTimeField(null=True)
    deletedByUserId = models.BigIntegerField(null=True)

class UserAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "account")
