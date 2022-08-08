from typing import List, Any, Dict

from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth.models import User

from api.models import Package


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
    paginate_by: int = 2
    model = Package

    def get_template_names(self) -> List[str]:
        return ["explore.html"]


class PackageDetailView(DetailView):
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


class UserDetailView(DetailView):
    slug_field: str = "username"
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        target_user: User = context["user"]
        auth_user: User = self.request.user
        context["authenticated"] = target_user == auth_user

        page = self.request.GET.get("page", 1)

        packages = target_user.packages.all()
        collabs = target_user.collaborations.all()

        context["num_contribs"] = len(collabs)
        context["num_owned"] = len(packages)

        packages = (packages | collabs).distinct().order_by("-downloads")
        paginator = Paginator(packages, 5)

        context["page"] = paginator.page(page)

        return context


@login_required()
def manageAccount(request: HttpRequest) -> HttpResponse:
    return render(request, "manage_profile.html")
