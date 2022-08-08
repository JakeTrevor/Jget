from typing import Any
from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponseBase
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from api.models import Package


class isOwnerMixin(LoginRequiredMixin):
    slug_field: str = "name"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        package: Package = self.get_object()
        if package.is_owner(request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()
