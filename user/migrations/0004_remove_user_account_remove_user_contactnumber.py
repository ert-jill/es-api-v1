# Generated by Django 5.0 on 2024-01-15 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_account_user_contactnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contactNumber',
        ),
    ]
