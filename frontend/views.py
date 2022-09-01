from typing import List, Any, Dict

from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, TemplateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.contrib.auth.models import User

from api.models import Package
from frontend.forms import updateContribForm
from frontend.mixins import isOwnerMixin, SearchableListView


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'developers': User.objects.count(),
        'packages': Package.objects.count(),
    }
    return render(request, 'home.html', context=context)


class get_JGET(TemplateView):
    template_name = "get_jget.html"


class explore(SearchableListView):
    paginate_by: int = 5
    model = Package

    def get_template_names(self) -> List[str]:
        return ["explore.html"]


class viewPackage(DetailView):
    slug_field: str = "name"
    model = Package
    template_name = "package.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        package: Package = context["package"]
        user = self.request.user
        context["is_owner"] = package.is_owner(user)
        context["is_contributor"] = package.is_contributor(user)

        return context

    def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        response = super().render_to_response(context, **response_kwargs)

        def handleCookie():
            package: Package = self.get_object()
            package.views += 1
            package.save()
            response.set_cookie("lastVisit", datetime.now())

        if not ("lastVisit" in self.request.COOKIES):
            handleCookie()
        else:
            lastVisit = self.request.COOKIES["lastVisit"]
            lastVisit = datetime.strptime(lastVisit[:-7], "%Y-%m-%d %H:%M:%S")
            delta: timedelta = (datetime.now() - lastVisit)
            if delta.days > 0:
                handleCookie()

        return response


class deletePackage(isOwnerMixin, DeleteView):
    model = Package
    template_name = "delete.html"


class transferOwnership(UpdateView):
    slug_field: str = "name"
    model = Package
    fields = ["creator"]
    template_name = "update.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Transfer Ownership"
        return context


class addContributor(UpdateView):
    slug_field: str = "name"
    model = Package
    form_class = updateContribForm
    template_name = "update.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Manage Contributors"
        return context


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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if (self.get_object() == request.user):
            return redirect("frontend:manage_account")
        return super().get(request, *args, **kwargs)


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
