from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response as apiResponse
from rest_framework.decorators import api_view
from api.models import Package
from api.serializers import PackageSerializer

# Create your views here.


@api_view(['GET'])
def getPackage(request: HttpRequest, package_name: str) -> apiResponse:
    package = get_object_or_404(Package, name=package_name)
    serializer = PackageSerializer(package, exclude=["authors"])
    return apiResponse(serializer.data)


@api_view(['POST'])
def createPackage(request: HttpRequest) -> apiResponse:
    serializer = PackageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return apiResponse(serializer.data)
