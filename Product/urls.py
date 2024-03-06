from django.urls import path
from .views import BrandView, CategoryView, SubCategoryView

urlpatterns = [
    path("brands/", BrandView.getBrands, name="getAllBrands"),
    path("brands/<id_>/", BrandView.getSpecificBrand, name="getSpecificBrand"),


    path("categories/", CategoryView.getCategories, name="getAllCategories"),
    path("category/<id_>/", CategoryView.getSpecificCategory, name="getSpecificCategory"),

    path("subCategories/", SubCategoryView.getAllSubCategories, name="getAllSubCategories"),
    path("categories/<id_>/subCategories/", SubCategoryView.getAllSubCategoriesInCategory, name="getAllSubCategoriesInCategory"),
    path("subCategories/<id_>/", SubCategoryView.getSpecificSubCategory, name="getSpecificSubCategory"),
]

