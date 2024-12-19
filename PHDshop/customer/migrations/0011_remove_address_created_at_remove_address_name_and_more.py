# Generated by Django 5.0.6 on 2024-12-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='address',
            name='name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
