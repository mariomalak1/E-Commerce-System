from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from project.utilis import getDataFromPaginator
from .serializer import BrandSerializer
from .models import Brand
# Create your views here.

class BrandView:
    @staticmethod
    @api_view(["GET"])
    def getBrands(request):
        brands = Brand.objects.all()
        allData = getDataFromPaginator(request, brands)

        if allData:
            required_page, per_page, paginator, metaData = allData
            serializer = BrandSerializer(paginator.get_page(required_page), many=True)
            response = {"result": paginator.count, "metadata": metaData, "data": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"errors":"put valid page number and per page number"}, status=status.HTTP_400_BAD_REQUEST)

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
