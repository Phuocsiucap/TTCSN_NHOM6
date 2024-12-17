# serializers.py
from rest_framework import serializers
from .models import Voucher, VoucherUser

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ['id', 'title', 'discount_percentage', 'min_order_value', 'points_required', 'quantity', 'is_active']

class VoucherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherUser
        fields = ['id', 'user', 'voucher', 'points_used', 'quantity', 'redeemed_at', 'status', 'amount_paid']
