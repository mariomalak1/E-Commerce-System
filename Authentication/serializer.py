from abc import ABC

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password", "phone", "rePassword"]

    rePassword = serializers.CharField(required=True)

    def create_user(self):
        user_ = self.save()
        user_.set_password(self.data.get("password"))
        user_.save()
        return user_

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

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

    def is_valid(self, raise_exception=False):
        if self.partial:
            self.fields.get("email").validators = []
        return super().is_valid(raise_exception=raise_exception)

class UpdateUserPassword(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    rePassword = serializers.CharField(required=True)
