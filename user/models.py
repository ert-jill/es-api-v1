from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from user_type.models import UserType

#use to tag account for user
class UserUserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_user_account')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

#use to tag usertype to user
class UserUserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_user_type')
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
