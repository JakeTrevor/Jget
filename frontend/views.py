from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import User

from api.models import Package
# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    print(request.user)
    context = {
        'developers': User.objects.count(),
        'packages': Package.objects.count(),
    }
    return render(request, 'home.html', context=context)
