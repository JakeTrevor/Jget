from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('get_jget/', views.get_JGET.as_view(), name="get_JGET"),
    path('explore/', views.explore.as_view(), name="explore"),
    path('manage_account', views.manageAccount, name="manage_account"),
    path('profile/<slug:slug>/', views.UserDetailView.as_view(), name="profile"),
]
