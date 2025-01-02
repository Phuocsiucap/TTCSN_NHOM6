from django.db import models
from good.models import Good
from customer.models import User

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=15)  # Changed size to accommodate country code
    password = models.CharField(max_length=128)  # Use CharField to store hashed passwords

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)  # Changed to CharField for city names
    district = models.CharField(max_length=30)
    detailed_address = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Promotion(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_name = models.CharField(max_length=50)
    discount_percentage = models.FloatField()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'admin')  # Lowercased field names

class GoodPromotion(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('good', 'promotion')  # Lowercased field names
