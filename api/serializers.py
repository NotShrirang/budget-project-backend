from api.models import (
    Department,
    CollegeUser,
    Activity,
    Transaction,
)
from rest_framework import serializers
from django.contrib import auth
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, SerializerMethodField, Serializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class CollegeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeUser
        fields = '__all__'

class RegisterSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    class Meta:
        model = CollegeUser
        fields = ['email','username','password','department','privilege']
    def validate(self, attrs):
        username = attrs.get('email', '')
        if not username.isalnum():
            raise ValidationError(self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return CollegeUser.objects.create_user(**validated_data)
    
class LoginSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    email = CharField(max_length=255, min_length=3)
    tokens = SerializerMethodField()
    def get_tokens(self, obj):
        user = CollegeUser.objects.get(username=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = CollegeUser
        fields = ['password','email','tokens']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class LogoutSerializer(Serializer):
    refresh = CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'