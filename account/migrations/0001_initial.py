# Generated by Django 5.0 on 2024-01-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('ownerName', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('contactNumber', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=250)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('createdByUserId', models.IntegerField(null=True)),
                ('updatedDate', models.DateTimeField(null=True)),
                ('deletedDate', models.DateTimeField(null=True)),
                ('deletedByUserId', models.IntegerField(null=True)),
            ],
        ),
    ]
