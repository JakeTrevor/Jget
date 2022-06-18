from rest_framework.request import Request as apiRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response as apiResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from api.models import Package
from api.serializers import PackageSerializer

# Create your views here.


@api_view(['GET'])
def getPackage(request: apiRequest, package_name: str) -> apiResponse:
    package = get_object_or_404(Package, name=package_name)
    serializer = PackageSerializer(package)
    return apiResponse(serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
def createPackage(request: apiRequest) -> apiResponse:
    serializer = PackageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return apiResponse(serializer.data)
