# Generated by Django 4.1.7 on 2023-10-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodShop', '0017_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
