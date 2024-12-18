# serializers.py
from rest_framework import serializers
from .models import Voucher, VoucherUser

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherUser
        fields = '__all__'
