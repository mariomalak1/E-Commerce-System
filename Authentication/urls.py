from django.urls import path, include

from . import views

urlpatterns = [
    path("signin/", views.UserAuthentication.login, name="signin"),
    path("signup/", views.UserAuthentication.signup, name="signup"),
    path("getAllUsers/", views.UserAuthentication.getAllUsers, name="getAllUsers"),
    path("forgetPassword/", views.UserAuthentication.forgetPassword, name="forgetPassword"),
    path("verfiyResetPassword/", views.UserAuthentication.verfiyResetPassword, name="verfiyResetPassword"),
    path("resetPassword/", views.UserAuthentication.resetPassword, name="resetPassword"),
    path("updateUserData/", views.UserAuthentication.updateUserData, name="updateUserData"),
    path("updateLoggedUserPassword/", views.UserAuthentication.updateLoggedUserPassword, name="updateLoggedUserPassword"),
]