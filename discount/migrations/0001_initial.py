# Generated by Django 5.0 on 2024-02-13 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_useraccount'),
        ('order', '0019_alter_orderitem_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_type', models.CharField(max_length=25)),
                ('is_active', models.BooleanField(default=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discount_account', to='account.account')),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discount_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discount_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discount_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_discount_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_discount_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='discount.discount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.order')),
                ('order_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.orderitem')),
                ('updated_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_discount_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('order', 'order_item', 'discount')},
            },
        ),
    ]