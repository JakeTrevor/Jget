from unicodedata import name
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('', include(('frontend.urls', "frontend"))),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
