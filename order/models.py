from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from account.models import Account

from product.models import Product


class Order(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="orders_account"
    )  # acount who own the order
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    customer = models.CharField(
        max_length=255, null=True, blank=True
    )  # purchasing customer
    is_void = models.BooleanField(default=False)
    is_void_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="orders_voided_by",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="orders_created_by"
    )
    updated_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="orders_updated_by",
    )

    # Payment Information
    payment_method = models.CharField(
        max_length=50, null=True, blank=True
    )  # cash, card, wallet
    payment_status = models.CharField(
        max_length=20, null=True, blank=True
    )  # pending, completed
    payment_reference_no = models.CharField(
        max_length=100, null=True, blank=True
    )  # payment reference

    # Shipping Information
    shipping_address = models.TextField(null=True, blank=True)
    shipping_status = models.CharField(max_length=20, null=True, blank=True)
    tracking_info = models.CharField(max_length=100, null=True, blank=True)
    # Order Status
    order_status = models.CharField(
        max_length=20, null=True, blank=True, default=""
    )  # open, ongoing, billout, closed


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, to_field='sku', db_column='product_sku'
    )  # reference for the product record
    product_name = models.CharField(max_length=255)  # product_name upon purchase
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # product_price upon purchase
    product_description = models.CharField(
        max_length=255, null=True, blank=True
    )  # product_description upon purchase
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # product_quantity upon purchase
    product_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )  # product_discount upon purchase
    product_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0.0
    )  # product_discount upon purchase
    is_void = models.BooleanField(default=False)  # product_is_void upon purchase
    is_void_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="order_items_voided_by",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_items_created_by"
    )
    updated_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="order_items_updated_by",
    )
    class Meta:
        unique_together = ('order', 'product')