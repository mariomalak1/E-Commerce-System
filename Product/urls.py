from django.urls import path
from .views import BrandView

urlpatterns = [
    path("brands/", BrandView.getBrands, name="getAllBrands"),
    path("brands/<id_>/", BrandView.getSpecificBrand, name="getSpecificBrand"),
]
