from abc import ABC

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password", "phone"]

    rePassword = serializers.CharField(required=True)

    def create_user(self):
        user_ = self.save()
        user_.set_password(self.data.get("password"))
        user_.save()
        return user_

class ForgetPassword(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    newPassword = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "phone"]