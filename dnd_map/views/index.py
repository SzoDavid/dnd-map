import json

from django.shortcuts import render, get_object_or_404

from PIL import Image

from dnd_imh.models import World
from dnd_map.models import Item, Coord
from dnd_map.views.functions import create_item_tree


def index(request, world_pk):
    world = get_object_or_404(World, pk=world_pk)

    items = []
    original_width = None

    if bool(world.main_map):
        map_img = Image.open(world.main_map)
        original_width = map_img.width
        map_img.close()

    if request.user.is_authenticated:
        item_roots = Item.objects.filter(parent__isnull=True)
        coords = Coord.objects.all().order_by('-z_axis')
    else:
        item_roots = Item.objects.filter(parent__isnull=True, discovered=True)
        coords = Coord.objects.filter(item__discovered=True).order_by('-z_axis')

    for item_root in item_roots:
        items.append(create_item_tree(world, item_root,
                                      not request.user.is_authenticated,
                                      world.max_item_tree_display_depth - 1))

    data = {'max_depth': world.max_item_tree_display_depth,
            'items': items}

    context = {
        'world': world,
        'map_original_width': original_width,
        'items': json.dumps(data),
        'coords': coords,
    }

    return render(request, 'dnd_map/index/index.html/', context)
