import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User, ResetCode
from .serializer import RegisterSerializer, ForgetPassword,\
    UserSerializer, ResetCodeSerializer, ResetPasswordSerializer, SignInSerializer, UpdateUserPassword
from .utils import resetPasswordSendMail, getDataFromPaginator
from django.contrib.auth import authenticate, login, logout
# Create your views here.


class UserAuthentication:
    @staticmethod
    def get_token_or_none(request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if not authorization_header:
            authorization_header = request.data.get("token")
            if not authorization_header:
                return None
        try:
            # Split the header value to extract the token
            auth_type, token = authorization_header.split(' ')
        except:
            token = authorization_header

        if token:
            token_ = Token.objects.filter(key=token).first()
            if token_:
                return token_

        return None

    @staticmethod
    @api_view(["GET"])
    def token_check_found(request):
        token_ = UserAuthentication.get_token_or_none(request)
        if token_ is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        token_required = Token.objects.filter(key=token_).first()
        if token_required:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
                    token = Token.objects.filter(user=user).first()
                    if not token:
                        token = Token.objects.create(user=user)
                else:
                    return Response({"message":"invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "user login succssfully", "token":token.key}, status=status.HTTP_200_OK)
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
            if serializer.data.get("rePassword") == serializer.data.get("password"):
                user = User(email=serializer.data.get("email"))
                user.set_password(serializer.data.get("password"))
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors":"password not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # change user data only if he is logged
    @staticmethod
    @api_view(["PATCH"])
    def updateUserData(request):
        token = UserAuthentication.get_token_or_none(request)
        if token:
            serializer = UserSerializer(data=request.data, instance=token.user, partial=True)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                user = User.objects.filter(email=email).first()
                if user:
                    if user != token.user:
                        return Response({"errors": "this email is not yours"})
                user = serializer.update(instance=token.user, validated_data=serializer.validated_data)
                userSerializer = UserSerializer(user)
                return Response(userSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "you must authorize"}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    @api_view(["PATCH"])
    def updateLoggedUserPassword(request):
        token = UserAuthentication.get_token_or_none(request)
        if token:
            serializer = UpdateUserPassword(data=request.data)
            if serializer.is_valid():
                currentPassword = serializer.validated_data.get("currentPassword")
                password = serializer.validated_data.get("password")
                rePassword = serializer.validated_data.get("rePassword")
                user = token.user
                if user.check_password(currentPassword):
                    if password == rePassword:
                        user.set_password(password)
                        user.save()
                        userSerializer = UserSerializer(user)
                        response = {"user":userSerializer.data, "token":token.key}
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        return Response({"errors":"password not match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({"errors": "current password not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "you must authorize"}, status=status.HTTP_401_UNAUTHORIZED)


    # rest password functions
    @staticmethod
    @api_view(["GET"])
    def forgetPassword(request):
        data = request.data
        serializer = ForgetPassword(data=data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data.get("email")).first()
            if user:
                if user.is_authenticated:
                    logout(request)
                resetCode = ResetCode.objects.filter(resetUser=user).first()
                if resetCode:
                    resetCode.delete()

                resetCode = ResetCode(resetUser=user)
                resetCode.save()
                # send reset code to customer by email
                resetPasswordSendMail(resetCode, user)
                return Response({"message": "Reset code sent to your email"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": "No user with this email"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    def verfiyResetPassword(request):
        data = request.data
        serializer = ResetCodeSerializer(data=data)
        if serializer.is_valid():
            resetCodeObj = ResetCode.objects.filter(resetUser__email=serializer.validated_data.get("email")).first()
            if resetCodeObj:
                if serializer.validated_data.get("code") == resetCodeObj.generatedCode:
                    if not resetCodeObj.isCodeExpired():
                        resetCodeObj.confirmedTime = datetime.datetime.now()
                        resetCodeObj.save()
                        return Response({"message":"code is correct, you can now reset your password"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"errors":"Reset code has expired"})
                else:
                    return Response({"errors":"Reset code is invalid"})
            else:
                return Response({"errors": "no forget password requesed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    def resetPassword(request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"errors":"this email not registred before"}, status=status.HTTP_400_BAD_REQUEST)
            resetCode = ResetCode.objects.filter(resetUser=user).first()
            if resetCode:
                if resetCode.confirmedTime:
                    newPassword = serializer.validated_data.get("newPassword")
                    user.set_password(newPassword)
                    user.save()
                    resetCode.delete()
                    return Response({"message":"password successfully changed"}, status=status.HTTP_200_OK)
                else:
                    return Response({"errors":"the reset code not verfied yet"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"errors": "no forget password requested"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # only if he is an admin
    @staticmethod
    @api_view(["GET"])
    # decorator that check on authorization
    def getAllUsers(reuqest):
        users = User.objects.all()
        allData = getDataFromPaginator(reuqest, users)

        if allData:
            required_page, per_page, paginator = allData
            serializer = UserSerializer(paginator.get_page(required_page), many=True)
            metaData = {"numberOfPages":paginator.num_pages, "currentPage": required_page, "perPage":per_page}
            response = {"result": paginator.count, "metadata": metaData, "data": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"errors":"put valid page number and per page number"}, status=status.HTTP_400_BAD_REQUEST)
