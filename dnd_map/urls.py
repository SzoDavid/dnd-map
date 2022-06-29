from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dnd_map'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('help', views.help_page, name='help'),
    path('login', auth_views.LoginView.as_view(template_name='dnd_map/admin/login.html', next_page='/dnd/',
                                               redirect_authenticated_user=True), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('new', views.new, name='new'),
    path('<int:item_pk>/new', views.new, name='new'),
    path('<int:item_pk>/edit', views.edit, name='edit'),
    path('<int:item_pk>/togglediscovered', views.toggle_discovered, name='toggle_discovered'),
    path('<int:item_pk>/toggledescription', views.toggle_description, name='toggle_description'),
    path('<int:item_pk>/addappearance', views.new_coord, name='new_coord'),
    path('<int:coord_pk>/editappearance', views.edit_coord, name='edit_coord'),
    path('<str:item_type>/<str:item_name>', views.items, name='details')
]
