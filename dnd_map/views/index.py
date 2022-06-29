import json

from django.shortcuts import render

from PIL import Image
from os import path

# from dnd_map.models import City, Kingdom, Place, TerrainCoords, Terrain

SITE_ROOT = path.dirname(path.realpath(__file__))


def index(request):
    # config = json.load(open(SITE_ROOT + '/../config.json'))
    #
    # is_map_set = config['main_map']['path'] != ''
    #
    # original_width = None
    #
    # if is_map_set:
    #     map_img = Image.open(SITE_ROOT + '/../static/dnd_map/images/maps/' + config['main_map']['path'])
    #     original_width = map_img.width
    #     map_img.close()
    #
    # if request.user.is_authenticated:
    #     places_list = Place.objects.all()
    #     cities_list = City.objects.all()
    #     kingdoms_list = Kingdom.objects.all()
    # else:
    #     places_list = Place.objects.filter(discovered=True)
    #     cities_list = City.objects.filter(discovered=True)
    #     kingdoms_list = Kingdom.objects.filter(discovered=True)
    #
    # context = {
    #     'is_map_set': is_map_set,
    #     'map_original_width': original_width,
    #     'world_name': config['main_map']['world_name'],
    #     'map_path': '/dnd_map/images/maps/' + config['main_map']['path'],
    #     'places':  places_list,
    #     'cities': cities_list,
    #     'kingdoms': kingdoms_list,
    #     'terrain_coords': TerrainCoords.objects.filter(location='IN'),
    #     'terrains': Terrain.objects.all(),
    # }
    #
    # return render(request, 'dnd_map/index/index.html/', context)
    return


def about(request):
    return render(request, 'dnd_map/index/about.html/')


def help_page(request):
    model = 'none'

    if 'model' in request.GET:
        model = request.GET['model']

    return render(request, 'dnd_map/index/help.html/', {'model': model})
