from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from api.models import Package


class packageMixin():
    slug_field: str = "name"


class isOwnerMixin(packageMixin, LoginRequiredMixin):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        package: Package = self.get_object()
        if package.is_owner(request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class SearchableListView(ListView):
    """A List view which modifies the queryset based on the search term in the "GET".
        search term name is specified as self.search_key_name
    """

    search_key_name = "search"

    def get_queryset(self):
        packageName = self.request.GET.get(self.search_key_name, "")
        queryset = super().get_queryset()

        if packageName:
            queryset = queryset.filter(name__icontains=packageName)
        return queryset
