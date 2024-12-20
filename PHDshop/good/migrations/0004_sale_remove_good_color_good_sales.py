# Generated by Django 5.0.6 on 2024-12-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good', '0003_alter_good_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='good',
            name='color',
        ),
        migrations.AddField(
            model_name='good',
            name='sales',
            field=models.ManyToManyField(blank=True, related_name='goods', to='good.sale'),
        ),
    ]
