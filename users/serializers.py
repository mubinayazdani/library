from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import PasswordReset, Contact

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password_1 = serializers.CharField(required=True, write_only=True)
    password_2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password_1', 'password_2')

        # extra_kwargs = {
        #
        #     'first_name': {'required': False},
        #     'last_name': {'required': False}
        # }

    def validate(self, attrs):
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError({
                'password': 'Passwords did not match.'
            })

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data.get['first_name',''],
            # last_name=validated_data.get['last_name',''],
            password=validated_data['password_1']
        )

        user.set_password(validated_data['password_1'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username:
            raise serializers.ValidationError({'username': 'Username is required.'})

        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({'password': 'Invalid username or password.'})

        return attrs


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['user', 'token', 'created_at', 'expires_at']

    def create(self, validated_data):
        password_reset = PasswordReset.objects.create(user=validated_data.get('user'))
        return password_reset


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
