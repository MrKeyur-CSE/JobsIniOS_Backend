from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=50, min_length=8, write_only=True,
        style={'input_type': 'password'})
    password2 = serializers.CharField(
        max_length=50, min_length=8, write_only=True,
        style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number',
                  'password', 'password2', 'address']

    def validate(self, attrs):
        email = attrs.get('email', '')
        full_name = attrs.get('full_name', '')
        phone_number = attrs.get('phone_number', '')
        address = attrs.get('address', '')

        attrs['username'] = email

        if not len(address) > 10:
            raise serializers.ValidationError('address is not correct')

        return attrs

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError('Passwords does not match')

        del validated_data['password2']
        validated_data['password'] = make_password(
            validated_data.get('password'))

        return CustomUser.objects.create(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(
        max_length=69, min_length=8, write_only=True,
        style={'input_type': 'password'})
    id = serializers.IntegerField(read_only=True)
    tokens = serializers.CharField(
        max_length=255, min_length=5, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid Credentials, Try again !')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled!')

        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens(),
        }

        # return super().validate(self)
