# Generated by Django 5.0.6 on 2025-01-01 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0008_order_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Đang xử lý', max_length=50),
        ),
    ]
