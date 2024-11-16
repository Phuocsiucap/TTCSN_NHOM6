from django.db import models
# Create your models here.


class User(models.Model):
    fullName = models.CharField(max_length=255)
    email = models.CharField(max_length=255,  unique=True)
    password = models.CharField(max_length=255)
    userType = models.CharField(max_length=50, default="Silver User", blank=True)
    loyaltyPoints = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

