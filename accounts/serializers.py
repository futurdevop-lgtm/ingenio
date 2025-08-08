from rest_framework import serializers
from django.contrib.auth import get_user_model
import pyotp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'location', 'two_factor_enabled']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, help_text='Mot de passe (min. 8 caractères)')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TwoFASetupSerializer(serializers.Serializer):
    secret = serializers.CharField(read_only=True)
    otp_auth_url = serializers.CharField(read_only=True)

    def create(self, validated_data):  # not used
        raise NotImplementedError


class TwoFAVerifySerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(attrs['code']):
            raise serializers.ValidationError('Code TOTP invalide')
        return attrs