from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:kingdom>', views.kingdoms, name='kingdoms'),
    path('<str:kingdom>/<str:city>', views.cities, name='cities'),
    path('<str:kingdom>/<str:city>/<str:place>', views.places, name='places'),
]
