from django.urls import path

from . import views

urlpatterns = [
    path("get/<slug:package_name>/", views.getPackage),
    path("upload/", views.createPackage),
]
