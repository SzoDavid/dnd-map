import json

from django.shortcuts import render

from PIL import Image
from os import path

from django.urls import reverse

from dnd_map.models import Item, Coord

SITE_ROOT = path.dirname(path.realpath(__file__))


def create_item_node(item):
    return {
        'name': item.name,
        'details': reverse('dnd_map:details', args=(item.type, item.name)),
        'edit': reverse('dnd_map:edit', args=(item.pk,)),
        'discovered': item.discovered,
        'toggle_discovered': reverse('dnd_map:toggle_discovered', args=(item.pk,)),
        'description': item.show_description,
        'toggle_description': reverse('dnd_map:toggle_description', args=(item.pk,)),
        'add_child': reverse('dnd_map:new', args=(item.pk,)),
        'children': [],
    }


def create_item_tree(item_root, discovered, depth):
    node = create_item_node(item_root)

    if depth == 0:
        return node

    if discovered:
        items = item_root.item_set.filter(discovered=True)
    else:
        items = item_root.item_set.all()

    if items.count() == 0:
        return node

    for item in items:
        node['children'].append(create_item_tree(item, discovered, depth - 1))

    return node


def index(request):
    config = json.load(open(SITE_ROOT + '/../config.json'))

    is_map_set = config['main_map']['path'] != ''
    max_display_depth = config['max_item_display_depth']

    items = []
    original_width = None

    if is_map_set:
        map_img = Image.open(SITE_ROOT + '/../static/dnd_map/images/maps/' + config['main_map']['path'])
        original_width = map_img.width
        map_img.close()

    if request.user.is_authenticated:
        item_roots = Item.objects.filter(parent__isnull=True)
        coords = Coord.objects.all()
    else:
        item_roots = Item.objects.filter(parent__isnull=True, discovered=True)
        coords = Coord.objects.filter(item__discovered=True)

    for item_root in item_roots:
        items.append(create_item_tree(item_root, not request.user.is_authenticated, max_display_depth - 1))

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
