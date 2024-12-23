from rest_framework import serializers
from .models import Order, OrderGood
from Voucher.models import Voucher

class OrderSerializer(serializers.ModelSerializer):
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all(), write_only=True)  # Chỉ cho phép gửi ID voucher
    class Meta:
        model = Order
        fields = '__all__'
class OrderGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGood
        fields = ['order', 'good', 'quantity']
