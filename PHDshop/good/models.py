from django.db import models
from rest_framework import serializers
class Brand(models.Model):
    brandName = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
class Category(models.Model):
    categoryName = models.CharField(max_length=255)


class Good(models.Model):
    id = models.AutoField(primary_key=True)
    goodName = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    color = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)

class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['id', 'goodName', 'specifications', 'image', 'color', 'amount', 'price', 'category', 'brand']