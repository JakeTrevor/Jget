from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as apiRequest
from rest_framework.response import Response as apiResponse
from rest_framework.decorators import api_view, permission_classes

from api.models import Package
from api.serializers import PackageSerializer

# Create your views here.


@api_view(['GET'])
def getPackage(request: apiRequest, package_name: str) -> apiResponse:
    package = get_object_or_404(Package, name=package_name)
    serializer = PackageSerializer(package)

    package.downloads += 1
    package.save()

    return apiResponse(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPackage(request: apiRequest, package_name="") -> apiResponse:
    pkg = Package.objects.filter(name=package_name).first()

    serializer = PackageSerializer(pkg, data=request.data)
    if serializer.is_valid(raise_exception=True):
        pkg = serializer.save(creator=request.user)

    return apiResponse(serializer.data)
