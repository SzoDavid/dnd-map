import json

from django.shortcuts import render

from PIL import Image
from os import path

from dnd_map.models import Item, Coord
from dnd_map.views.functions import create_item_tree

SITE_ROOT = path.dirname(path.realpath(__file__))


def index(request):
    config = json.load(open(SITE_ROOT + '/../config.json'))

    is_map_set = config['main_map']['path'] != ''

    items = []
    original_width = None

    if is_map_set:
        map_img = Image.open(SITE_ROOT + '/../static/dnd_map/images/maps/' + config['main_map']['path'])
        original_width = map_img.width
        map_img.close()

    if request.user.is_authenticated:
        item_roots = Item.objects.filter(parent__isnull=True)
        coords = Coord.objects.all().order_by('-z_axis')
    else:
        item_roots = Item.objects.filter(parent__isnull=True, discovered=True)
        coords = Coord.objects.filter(item__discovered=True).order_by('-z_axis')

    for item_root in item_roots:
        items.append(create_item_tree(item_root, not request.user.is_authenticated, config['max_item_display_depth'] - 1))

    context = {
        'is_map_set': is_map_set,
        'map_original_width': original_width,
        'world_name': config['main_map']['world_name'],
        'map_path': '/dnd_map/images/maps/' + config['main_map']['path'],
        'items': json.dumps(items),
        'coords': coords,
    }

    return render(request, 'dnd_map/index/index.html/', context)


def about(request):
    return render(request, 'dnd_map/index/about.html/')


def help_page(request):
    model = 'none'

    if 'model' in request.GET:
        model = request.GET['model']

    return render(request, 'dnd_map/index/help.html/', {'model': model})
