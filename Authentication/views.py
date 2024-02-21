from rest_framework import response
from rest_framework.decorators import api_view

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
        pass


    # only if he is an admin
    @staticmethod
    def getAllUsers(reuqest):
        pass