from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import settings

urlpatterns = [
    path('', include('dnd_imh.urls')),
    path('world/', include('dnd_map.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
