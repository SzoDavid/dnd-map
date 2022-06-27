from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dnd_map'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='dnd_map/admin/login.html', next_page='/dnd/',
                                               redirect_authenticated_user=True), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('<str:settlement_type>/<int:settlement_id>/switchdiscovered', views.switch_discovered,
         name='switch_discovered'),
    path('<str:kingdom>', views.kingdoms, name='kingdoms'),
    path('<str:kingdom>/<str:city>', views.cities, name='cities'),
    path('<str:kingdom>/<str:city>/<str:place>', views.places, name='places'),
]
