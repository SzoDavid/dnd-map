import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from PIL import Image

from django.urls import reverse

from dnd_imh.models import World
from dnd_map.models import Item, Coord
from dnd_map.views import create_item_tree


def items(request, world_pk, item_pk):
    world = get_object_or_404(World, pk=world_pk)

    item = get_object_or_404(Item, pk=item_pk)

    original_width = None
    item_list = []

    if bool(item.map):
        map_img = Image.open(item.map)
        original_width = map_img.width
        map_img.close()

    if request.user.is_authenticated:
        item_roots = Item.objects.filter(parent=item)
        coords = Coord.objects.all().order_by('-z_axis')
        appearances = Coord.objects.filter(item=item)
    else:
        item_roots = Item.objects.filter(parent=item, discovered=True)
        coords = Coord.objects.filter(item__discovered=True).order_by('-z_axis')
        appearances = Coord.objects.filter(item=item, location__discovered=True)

    for item_root in item_roots:
        item_list.append(create_item_tree(world, item_root,
                                          not request.user.is_authenticated,
                                          world.max_item_tree_display_depth - 1))

    data = {'max_depth': world.max_item_tree_display_depth,
            'items': item_list}

    context = {
        'world': world,
        'item': item,
        'map_original_width': original_width,
        'items': json.dumps(data),
        'coords': coords,
        'appearances': appearances,
    }

    return render(request, 'dnd_map/details/item.html', context)


def search(request, world_pk):
    if request.method == 'POST':
        search_value = request.POST['search']

        if request.user.is_authenticated:
            item_query = Item.objects.filter(Q(name__icontains=search_value, world__pk=world_pk) |
                                             Q(type__icontains=search_value, world__pk=world_pk))
        else:
            item_query = Item.objects.filter(Q(name__icontains=search_value, world__pk=world_pk, discovered=True) |
                                             Q(type__icontains=search_value, world__pk=world_pk, discovered=True))

        result = {
            'auth': request.user.is_authenticated,
            'query': [],
        }
        for item in item_query:
            result['query'].append({
                'name': item.name,
                'type': item.type,
                'details': reverse('dnd_map:details', args=(world_pk, item.pk)),
                'edit': reverse('dnd_map:edit', args=(world_pk, item.pk)),
                'discovered': item.discovered,
                'toggle_discovered': reverse('dnd_map:toggle_discovered', args=(world_pk, item.pk)),
                'description': item.show_description,
                'toggle_description': reverse('dnd_map:toggle_description', args=(world_pk, item.pk)),
                'add_child': reverse('dnd_map:new', args=(world_pk, item.pk)),
            })
        return JsonResponse(result)
    else:
        return render(request, 'dnd_map/details/search.html', {'world': get_object_or_404(World, pk=world_pk)})
