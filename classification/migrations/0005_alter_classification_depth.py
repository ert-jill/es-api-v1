# Generated by Django 5.0 on 2024-02-22 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0004_alter_classification_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='depth',
            field=models.PositiveBigIntegerField(),
        ),
    ]