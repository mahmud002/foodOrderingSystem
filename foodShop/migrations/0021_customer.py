# Generated by Django 4.1.7 on 2024-12-01 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodShop', '0020_remove_order_customer_phone_number_order_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]