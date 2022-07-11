from django.urls import path

from . import views


app_name = 'dnd_map'
urlpatterns = [
    path('<int:world_pk>', views.index, name='index'),
    path('<int:world_pk>/new', views.new, name='new'),
    path('<int:world_pk>/search', views.search, name='search'),
    path('<int:world_pk>/<int:item_pk>', views.items, name='details'),
    path('<int:world_pk>/<int:item_pk>/new', views.new, name='new'),
    path('<int:world_pk>/<int:item_pk>/edit', views.edit, name='edit'),
    path('<int:world_pk>/<int:item_pk>/togglediscovered', views.toggle_discovered, name='toggle_discovered'),
    path('<int:world_pk>/<int:item_pk>/toggledescription', views.toggle_description, name='toggle_description'),
    path('<int:world_pk>/<int:item_pk>/addappearance', views.new_coord, name='new_coord'),
    path('<int:world_pk>/<int:coord_pk>/editappearance', views.edit_coord, name='edit_coord'),
    path('<int:world_pk>/<str:object_type>/<int:object_pk>/remove/<path:redirect>', views.remove, name='remove'),
]
