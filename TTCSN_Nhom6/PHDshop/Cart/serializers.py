from rest_framework import serializers
from .models import Cart, CartGood

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'  

class CartGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartGood
        fields = '__all__'  
