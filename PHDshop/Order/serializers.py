from rest_framework import serializers
from .models import Order, OrderGood
from Voucher.models import Voucher
from good.models import Good
from Voucher.models import Voucher
from customer.models import User
<<<<<<< HEAD
from django.contrib.auth.models import User as Admin
from vnpay_python.models import Payment

=======
from good.serializer import GoodSerializer
>>>>>>> cdafa0598fb7f5a66316a4dfe448738d2159ae61
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset =User.objects.all())
    admin = serializers.PrimaryKeyRelatedField(queryset =Admin.objects.all())
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all(), required=False)  
    pay = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only= True)
    class Meta:
        model = Order
        fields = '__all__'
class OrderGoodSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    good = serializers.PrimaryKeyRelatedField(queryset =Good.objects.all() )
=======
    good = serializers.PrimaryKeyRelatedField(queryset =Good.objects.all())
    # good=GoodSerializer()
    # order=OrderSerializer()
>>>>>>> cdafa0598fb7f5a66316a4dfe448738d2159ae61
    class Meta:
        model = OrderGood
        fields = ['order', 'good', 'quantity']
