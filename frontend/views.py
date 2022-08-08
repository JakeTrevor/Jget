from typing import List, Any, Dict

from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.contrib.auth.models import User

from api.models import Package
from frontend.mixins import isOwnerMixin


def index(request: HttpRequest) -> HttpResponse:
    print(request.user)
    context = {
        'developers': User.objects.count(),
        'packages': Package.objects.count(),
    }
    return render(request, 'home.html', context=context)


class get_JGET(TemplateView):
    template_name = "get_jget.html"


class explore(ListView):
    paginate_by: int = 5
    model = Package

    def get_template_names(self) -> List[str]:
        return ["explore.html"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["list_title"] = "Popular Packages"
        return context


class viewPackage(DetailView):
    slug_field: str = "name"
    model = Package
    template_name = "package.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user = self.request.user
        package: Package = context["package"]
        context["is_owner"] = package.is_owner(user)
        context["is_contributor"] = package.is_contributor(user)
        return context


class deletePackage(isOwnerMixin, DeleteView):
    model = Package
    template_name = "delete.html"


class UserDetailView(DetailView):
    slug_field: str = "username"
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user: User = context["user"]

        page = self.request.GET.get("page", 1)

        packages = user.packages.all()
        collabs = user.collaborations.all()

        context["num_contribs"] = len(collabs)
        context["num_owned"] = len(packages)

        packages = (packages | collabs).distinct().order_by("-downloads")
        paginator = Paginator(packages, 5)

        context["page"] = paginator.page(page)

        return context


class manageAccount(LoginRequiredMixin, TemplateView):
    template_name = "manage_account.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user: User = self.request.user

        page = self.request.GET.get("page", 1)

        packages = user.packages.all()
        collabs = user.collaborations.all()

        context["num_contribs"] = len(collabs)
        context["num_owned"] = len(packages)

        packages = (packages | collabs).distinct().order_by("-downloads")
        paginator = Paginator(packages, 5)

        context["page"] = paginator.page(page)

        return context
