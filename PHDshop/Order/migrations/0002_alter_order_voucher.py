# Generated by Django 5.0.6 on 2024-12-26 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
        ('Voucher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Voucher.voucher'),
        ),
    ]
