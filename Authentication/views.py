import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import User, ResetCode
from .serializer import RegisterSerializer, ForgetPassword,\
    UserSerializer, ResetCodeSerializer, ResetPasswordSerializer, SignInSerializer
from .utils import resetPasswordSendMail
from django.contrib.auth import authenticate, login
# Create your views here.


class UserAuthentication:

    @staticmethod
    @api_view(["GET"])
    def login(request):
        serializer = SignInSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email).first()
            if user:
                user = authenticate(request, username=user.username, password=serializer.validated_data.get("password"))
                if user:
                    login(request, user)
                else:
                    return Response({"message":"invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "user login succssfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors":"no user with this email"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    def signup(request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if serializer.data.get("rePassword") == serializer.data.get("password"):
                user.set_password(serializer.data.get("password"))
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors":"password not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=tatus.HTTP_400_BAD_REQUEST)


    # change user data only if he is logged
    @staticmethod
    def updateUserData(request):
        pass

    # rest password functions
    @staticmethod
    def forgetPassword(request):
        data = request.data
        serializer = ForgetPassword(data=data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data.get("email")).first()
            if user:
                resetCode = ResetCode.objects.filter(user=user).first()
                if resetCode:
                    resetCode.delete()

                resetCode = ResetCode()
                resetCode.save()
                # send reset code to customer by email
                resetPasswordSendMail(resetCode, user)
                return Response({"message": "Reset code sent to your email"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": "No user with this email"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def verfiyResetPassword(request):
        data = request.data
        serializer = ResetCodeSerializer(data=data)
        if serializer.is_valid():
            resetCodeObj = ResetCode.objects.filter(user__email=serializer.validated_data.get("email")).first()
            if resetCodeObj:
                if serializer.validated_data.get("code") == resetCodeObj.generatedCode:
                    if not resetCodeObj.isCodeExpired():
                        resetCodeObj.confirmedTime = datetime.datetime.now()
                        resetCodeObj.save()
                    else:
                        return Response({"errors":"Reset code has expired"})
                else:
                    return Response({"errors":"Reset code is invalid"})
            else:
                return Response({"errors": "no forget password requesed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def resetPassword(request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"errors":"this email not registred before"}, status=status.HTTP_400_BAD_REQUEST)
            resetCode = ResetCode.objects.filter(user_=user).first()
            if resetCode:
                if resetCode.confirmedTime:
                    newPassword = serializer.validated_data.get("newPassword")
                    user.set_password(newPassword)
                    user.save()
                    return Response({"message":"password successfully changed"}, status=status.HTTP_200_OK)
                else:
                    return Response({"errors":"the reset code not verfied yet"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"errors": "no forget password requested"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # only if he is an admin
    @staticmethod
    # decorator that check on authorization
    def getAllUsers(reuqest):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
