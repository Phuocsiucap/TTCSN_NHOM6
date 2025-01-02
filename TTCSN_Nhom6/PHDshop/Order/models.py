from django.db import models
from customer.models import * 
from good.models import * 
from django.contrib.auth.models import User as Admin
from Voucher.models import Voucher

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    purchase_date = models.DateField(auto_now_add=True)  # Đặt mặc định là ngày hiện tại
    SHIPPING_STATUS_CHOICES = [
        ('Đang xử lý', 'Đang xử lý'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    shipping_status = models.CharField(max_length=50, choices=SHIPPING_STATUS_CHOICES, default='Đang xử lý')
    total_amount = models.FloatField()
    shipping_address = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)  # Admin có thể là null
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True) 

class OrderGood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'good')  # unique_together để tránh trùng lặp sản phẩm trong một đơn hàng
