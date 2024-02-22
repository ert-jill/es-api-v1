from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120)
    ownerName = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contactNumber = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    createdByUserId = models.BigIntegerField(null=True)
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
