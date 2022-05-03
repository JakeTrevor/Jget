from django.urls import path
from POC import views

app_name = "test"


urlpatterns = [
    path("", views.default),
]
