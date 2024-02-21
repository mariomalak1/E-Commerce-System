from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import User, ResetPassword
from .serializer import RegisterSerializer, ForgetPassword
# Create your views here.


class UserAuthentication:

    @staticmethod
    @api_view(["GET"])
    def login(request):
        pass

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
    def resetPassword(request):
        pass

    @staticmethod
    def verfiyResetPassword(request):
        pass

    @staticmethod
    def forgetPassword(request):
        data = request.data
        serializer = ForgetPassword(data=data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data.get("email")).first()
            if user:
                resetPassword = ResetPassword.objects.filter(user=user).first()
                if resetPassword:
                    resetPassword.delete()
                    resetPassword = ResetPassword()

                    # send reset code to customer by email

                    return Response
            else:
                return Response({"errors":"No user with this email"}, status=status.HTTP_400_BAD_REQUEST)

    # only if he is an admin
    @staticmethod
    def getAllUsers(reuqest):
        pass