# Generated by Django 5.0 on 2024-03-10 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_groupproduct_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='receipt_label',
            field=models.CharField(default='sample', max_length=50),
            preserve_default=False,
        ),
    ]