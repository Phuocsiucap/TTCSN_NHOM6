from django.db import models
from customer.models import * 
from good.models import * 
from django.contrib.auth.models import User as Admin
from Voucher.models import Voucher
from vnpay_python.models import Payment

class Order(models.Model):
    order_id = models.CharField(max_length=100,primary_key=True)
    purchase_date = models.DateTimeField(auto_now=True)
    SHIPPING_STATUS_CHOICES = [
<<<<<<< HEAD
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    shipping_status = models.CharField(max_length=50, choices=SHIPPING_STATUS_CHOICES, default='Đang xử lý')
    
    
=======
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Đã Giao', 'Đã Giao'),
        ('Đã xác nhận', 'Đã xác nhận'),
        ('Đang Giao', 'Đang Giao'),
        ('Đã Hủy', 'Đã Hủy'),
    ]
    shipping_status = models.CharField(max_length=50, choices=SHIPPING_STATUS_CHOICES, default='Chờ xác nhận')
>>>>>>> cdafa0598fb7f5a66316a4dfe448738d2159ae61
    total_amount = models.FloatField()
    shipping_address = models.CharField(max_length=100)
    updated_order_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)  # Admin có thể là null
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True) 
    pay = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderGood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'good')  # unique_together để tránh trùng lặp sản phẩm trong một đơn hàng
