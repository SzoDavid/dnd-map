from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dnd/', include('dnd_map.urls')),
    path('admin/', admin.site.urls),
]
