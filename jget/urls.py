from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def test(request):
    return HttpResponse("Placeholder for Jget")


urlpatterns = [
    path('', test),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
