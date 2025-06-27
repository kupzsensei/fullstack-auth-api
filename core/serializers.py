from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # token['password'] = user.password
        # ...

        return token

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username' , 'password' , 'password_confirm']

    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': "Passwords do not match!"})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data.pop('password_confirm')
        return super().create(validated_data)