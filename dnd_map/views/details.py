import json

from django.shortcuts import render, get_object_or_404
# from dnd_map.models import Kingdom, City, Place, TerrainCoords, Terrain

from PIL import Image
from os import path


SITE_ROOT = path.dirname(path.realpath(__file__))


# def kingdoms(request, kingdom):
#     # kingdom_object = get_object_or_404(Kingdom, name=kingdom)
#     #
#     # original_width = None
#     # places_list = []
#     #
#     # if bool(kingdom_object.map):
#     #     map_img = Image.open(kingdom_object.map)
#     #     original_width = map_img.width
#     #     map_img.close()
#     #
#     # if request.user.is_authenticated:
#     #     cities_list = kingdom_object.city_set.all()
#     #     for city in cities_list:
#     #         for place in city.place_set.all():
#     #             places_list.append(place)
#     # else:
#     #     cities_list = kingdom_object.city_set.filter(discovered=True)
#     #     for city in cities_list:
#     #         for place in city.place_set.filter(discovered=True):
#     #             places_list.append(place)
#     #
#     # context = {
#     #     'kingdom': kingdom_object,
#     #     'map_original_width': original_width,
#     #     'capital': kingdom_object.city_set.get(capital=True),
#     #     'cities': cities_list,
#     #     'places': places_list,
#     #     'terrain_coords': TerrainCoords.objects.filter(location='KI', kingdom=kingdom_object),
#     # }
#     #
#     # return render(request, 'dnd_map/details/kingdom.html', context)
#     return
#
#
# def cities(request, kingdom, city):
#     city_object = get_object_or_404(City, name=city, kingdom__name=kingdom)
#
#     original_width = None
#
#     if bool(city_object.map):
#         map_img = Image.open(city_object.map)
#         original_width = map_img.width
#         map_img.close()
#
#     if request.user.is_authenticated:
#         places_list = city_object.place_set.all()
#     else:
#         places_list = city_object.place_set.filter(discovered=True)
#
#     context = {
#         'city': city_object,
#         'map_original_width': original_width,
#         'places': places_list,
#         'terrain_coords': TerrainCoords.objects.filter(location='CI', city=city_object),
#     }
#
#     return render(request, 'dnd_map/details/city.html', context)
#
#
# def places(request, kingdom, city, place):
#     place_object = get_object_or_404(Place, name=place, city__name=city, city__kingdom__name=kingdom)
#
#     original_width = None
#
#     if bool(place_object.map):
#         map_img = Image.open(place_object.map)
#         original_width = map_img.width
#         map_img.close()
#
#     context = {
#         'place': place_object,
#         'map_original_width': original_width,
#     }
#
#     return render(request, 'dnd_map/details/place.html', context)
#
#
# def terrains(request, terrain):
#     terrain_object = get_object_or_404(Terrain, name=terrain)
#     config = json.load(open(SITE_ROOT + '/../config.json'))
#
#     context = {
#         'terrain': terrain_object,
#         'terrain_coords': terrain_object.terraincoords_set.all().order_by('terrain'),
#         'world_name': config['main_map']['world_name'],
#     }
#
#     return render(request, 'dnd_map/details/terrain.html', context)
