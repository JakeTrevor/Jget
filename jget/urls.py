from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def test():
    return HttpResponse("Placeholder for Jget")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test),
    path('api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
