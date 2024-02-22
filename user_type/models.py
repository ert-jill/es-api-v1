from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserType(models.Model):
    id = models.BigAutoField(primary_key=True)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_type_created_by"
    )
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_type_deleted_by",
    )
    updated_date = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_type_updated_by",
    )
