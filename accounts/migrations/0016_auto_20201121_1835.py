# Generated by Django 3.1.3 on 2020-11-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_customer_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=355, null=True),
        ),
    ]
