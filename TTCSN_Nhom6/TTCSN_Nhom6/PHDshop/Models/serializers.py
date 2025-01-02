from rest_framework import serializers
from .models import Admin, Category, Customer, Address, Product, Promotion, Brand, Contact, ProductPromotion

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['admin_id', 'admin_name', 'email', 'phone_number', 'password']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'full_name', 'email', 'phone_number', 'password', 'user_type', 'loyalty_points']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'country', 'city', 'district', 'detailed_address', 'customer']




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'price', 'technical_specifications', 'image', 'color', 'quantity', 'brand', 'category']

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['promotion_id', 'promotion_name', 'discount_percentage']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id', 'brand_name', 'description']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['customer', 'admin']




class ProductPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPromotion
        fields = ['product', 'promotion']
