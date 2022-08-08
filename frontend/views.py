from typing import List

from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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



@login_required()
def manageAccount(request: HttpRequest) -> HttpResponse:
    return render(request, "manage_profile.html")
