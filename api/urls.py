from django.urls import path

from . import views

urlpatterns = [
    path("get/<slug:package_name>/", views.getPackage),
    path("put/<slug:package_name>/", views.createPackage),
    path("put/", views.createPackage),
]
