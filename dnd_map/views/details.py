import json

from django.shortcuts import render, get_object_or_404

from PIL import Image
from os import path

from dnd_map.models import Item, Coord
from dnd_map.views import create_item_tree


SITE_ROOT = path.dirname(path.realpath(__file__))


def items(request, item_type, item_name):
    config = json.load(open(SITE_ROOT + '/../config.json'))

    item = get_object_or_404(Item, type=item_type, name=item_name)

    original_width = None
    item_list = []

    if bool(item.map):
        map_img = Image.open(item.map)
        original_width = map_img.width
        map_img.close()

    if request.user.is_authenticated:
        item_roots = Item.objects.filter(parent=item)
        coords = Coord.objects.all().order_by('-z_axis')
    else:
        item_roots = Item.objects.filter(parent=item, discovered=True)
        coords = Coord.objects.filter(item__discovered=True).order_by('-z_axis')

    for item_root in item_roots:
        item_list.append(create_item_tree(item_root,
                                          not request.user.is_authenticated,
                                          config['max_item_display_depth'] - 1))

    context = {
        'item': item,
        'map_original_width': original_width,
        'items': item_list,
        'coords': coords
    }

    return render(request, 'dnd_map/details/item.html', context)
