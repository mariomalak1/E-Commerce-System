from django.urls import path, include

from . import views

urlpatterns = [
    path("signin/", views.UserAuthentication.login, name="signin"),
    path("signup/", views.UserAuthentication.signup, name="signup"),
]