# Generated by Django 5.0 on 2024-02-22 20:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_account_createdbyuserid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='createdByUserId',
        ),
        migrations.AddField(
            model_name='account',
            name='created_by_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='account_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]