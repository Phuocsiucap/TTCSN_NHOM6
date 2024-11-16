# Generated by Django 5.0.6 on 2024-11-14 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Models', '0001_initial'),
        ('customer', '0006_alter_user_email'),
        ('good', '0003_alter_good_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('shipping_status', models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Processing', max_length=50)),
                ('total_amount', models.FloatField()),
                ('shipping_address', models.CharField(max_length=100)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.admin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderGood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='good.good')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Order.order')),
            ],
            options={
                'unique_together': {('order', 'good')},
            },
        ),
    ]
