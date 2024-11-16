from rest_framework import serializers
from .models import Order, OrderGood

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'purchase_date', 'shipping_status', 'total_amount', 'shipping_address', 'user', 'admin']

class OrderGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGood
        fields = ['order', 'good', 'quantity']
