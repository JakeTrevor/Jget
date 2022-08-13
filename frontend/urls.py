from django.urls import path

from frontend.views import *

urlpatterns = [
    path('', index, name="index"),
    path('get_jget/', get_JGET.as_view(), name="get_JGET"),
    path('explore/', explore.as_view(), name="explore"),

    path('package/<slug:slug>/', viewPackage.as_view(), name="package"),
    path('package/<slug:slug>/delete',
         deletePackage.as_view(), name="deletePackage"),
    path('package/<slug:slug>/transfer',
         transferOwnership.as_view(), name="transferOwnership"),
    path('package/<slug:slug>/addContributor',
         addContributor.as_view(), name="addContributor"),

    path('manage_account', manageAccount.as_view(), name="manage_account"),
    path('profile/<slug:slug>/', UserDetailView.as_view(), name="profile"),
]
