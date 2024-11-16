from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullName', 'email', 'password', 'userType', 'loyaltyPoints']

    def create(self, validated_data):
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.password = validated_data['password']
        return super(UserSerializer, self).update(instance, validated_data)