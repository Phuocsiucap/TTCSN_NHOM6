# Generated by Django 5.1.2 on 2024-10-23 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_user_loyaltypoints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phoneNumber',
        ),
    ]