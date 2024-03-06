from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator

# function that take paginator and try to get the required page number and per-page number
def getDataFromPaginator(request, objectsNeedToPaginate) -> "required_page, per_page, paginator, meta_data":
    try:
        required_page = request.GET.get("page", 1)
        per_page = request.GET.get("perPage", 10)

        paginator = Paginator(objectsNeedToPaginate, per_page)

        if objectsNeedToPaginate:
            if int(required_page) > paginator.num_pages:
                required_page = paginator.num_pages
            elif int(required_page) < 1:
                required_page = 1
            else:
                required_page = int(required_page)
        meta_data = {"numberOfPages": paginator.num_pages, "currentPage": required_page, "perPage": per_page}

        return (required_page, per_page, paginator, meta_data)
    except:
        return None


# defualt response for some views that have many objects in return
def defualtResponse(allData, SerializerName):
    if allData:
        required_page, per_page, paginator, metaData = allData
        serializer = SerializerName(paginator.get_page(required_page), many=True)
        response = {"result": paginator.count, "metadata": metaData, "data": serializer.data}
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({"errors": "put valid page number and per page number"}, status=status.HTTP_400_BAD_REQUEST)
