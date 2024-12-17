# Generated by Django 5.0.6 on 2024-12-17 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Voucher', '0001_initial'),
        ('customer', '0009_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_used', models.IntegerField()),
                ('quantity', models.IntegerField(default=1)),
                ('redeemed_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('redeemed', 'Redeemed'), ('expired', 'Expired')], default='redeemed', max_length=20)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redeemed_vouchers', to='customer.user')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voucher_users', to='Voucher.voucher')),
            ],
        ),
    ]
