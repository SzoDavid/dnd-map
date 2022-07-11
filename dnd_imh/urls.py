from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dnd_imh'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_user, name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='dnd_imh/user/login.html', next_page='/',
                                               redirect_authenticated_user=True), name='login'),
    path('about', views.about, name='about'),
    path('worlds', views.worlds, name='worlds')
]
