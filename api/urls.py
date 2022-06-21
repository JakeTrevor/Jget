from django.urls import path

from . import views

urlpatterns = [
    path("get/<slug:package_name>/", views.getPackage),
    path("put/", views.createPackage),
]
