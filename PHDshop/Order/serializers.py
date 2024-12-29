from rest_framework import serializers
from .models import Order, OrderGood
from Voucher.models import Voucher
from good.models import Good
from Voucher.models import Voucher
from customer.models import User
from good.serializer import GoodSerializer
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset =User.objects.all())
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all(), required=False)  
    class Meta:
        model = Order
        fields = '__all__'
class OrderGoodSerializer(serializers.ModelSerializer):
    good = serializers.PrimaryKeyRelatedField(queryset =Good.objects.all())
    # good=GoodSerializer()
    # order=OrderSerializer()
    class Meta:
        model = OrderGood
        fields = ['order', 'good', 'quantity']
