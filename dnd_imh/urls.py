from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dnd_imh'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_user, name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='dnd_imh/user/login.html', next_page='/',
                                               redirect_authenticated_user=True), name='login'),
    path('register', views.register_user, name='register_user'),
    path('about', views.about, name='about'),
    path('worlds', views.worlds, name='worlds'),
    path('createworld', views.create_world, name='create_world'),
    path('<int:world_pk>/editworld', views.edit_world, name='edit_world'),
    path('<int:world_pk>/removeworld', views.remove_world, name='remove_world'),
    path('users/<int:user_pk>', views.user, name='user')
]
