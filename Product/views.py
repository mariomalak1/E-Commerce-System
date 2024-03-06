from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from project.utilis import getDataFromPaginator, defualtResponse
from .serializer import BrandSerializer, CategorySerializer, SubCategorySerializer
from .models import Brand, Category, SubCategory
# Create your views here.

class BrandView:
    @staticmethod
    @api_view(["GET"])
    def getBrands(request):
        brands = Brand.objects.all()
        allData = getDataFromPaginator(request, brands)
        return defualtResponse(allData, BrandSerializer)


    @staticmethod
    @api_view(["GET"])
    def getSpecificBrand(request, id_):
        brand = Brand.objects.filter(ref=id_).first()
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def addBrand(request):
        pass


    @staticmethod
    def editBrand(request):
        pass


    @staticmethod
    def deleteBrand(request):
        pass


class CategoryView:
    @staticmethod
    @api_view(["GET"])
    def getCategories(request):
        categories = Category.objects.all()
        allData = getDataFromPaginator(request, categories)
        return defualtResponse(allData, CategorySerializer)

    @staticmethod
    @api_view(["GET"])
    def getSpecificCategory(request, id_):
        category = Category.objects.filter(ref=id_).first()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryView:
    @staticmethod
    @api_view(["GET"])
    def getAllSubCategories(request):
        subCategories = SubCategory.objects.all()
        allData = getDataFromPaginator(request, subCategories)

        return defualtResponse(allData, SubCategorySerializer)


    @staticmethod
    @api_view(["GET"])
    def getAllSubCategoriesInCategory(request, id_):
        subCategories = SubCategory.objects.filter(category__ref=id_).all()
        allData = getDataFromPaginator(request, subCategories)

        return defualtResponse(allData, SubCategorySerializer)


    @staticmethod
    @api_view(["GET"])
    def getSpecificSubCategory(request, id_):
        subCategories = SubCategory.objects.filter(ref=id_).first()
        serializer = SubCategorySerializer(subCategories)
        return Response(serializer.data, status=status.HTTP_200_OK)