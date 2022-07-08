from django.urls import path

from . import views


app_name = 'dnd_imh'
urlpatterns = [
    path('', views.index, name='index'),
]
