# Generated by Django 5.0 on 2024-01-20 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_orderitem_is_void_by_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='is_void_by_user',
        ),
    ]
