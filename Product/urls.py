from django.urls import path
from .views import BrandView, CategoryView

urlpatterns = [
    path("brands/", BrandView.getBrands, name="getAllBrands"),
    path("brands/<id_>/", BrandView.getSpecificBrand, name="getSpecificBrand"),


    path("categories/", CategoryView.getCategories, name="getAllBrands"),
    path("category/<id_>/", CategoryView.getSpecificCategory, name="getSpecificBrand"),
]

