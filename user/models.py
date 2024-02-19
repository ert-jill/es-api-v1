from django.db import models
from django.contrib.auth.models import User

from user_type.models import UserType

class UserUserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
