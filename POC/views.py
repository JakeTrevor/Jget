from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def default(req: HttpRequest):
    return HttpResponse("<h1>hi there from test app</h1>")
