# Generated by Django 4.1.7 on 2023-10-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodShop', '0016_order_order_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]