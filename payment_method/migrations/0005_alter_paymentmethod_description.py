# Generated by Django 5.0 on 2024-02-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_method', '0004_paymentmethod_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]