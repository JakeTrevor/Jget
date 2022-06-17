from knox import views as knox_views
from django.urls import path

from .views import LoginView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='knox_login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
