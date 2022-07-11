import json
import os

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from dnd_imh.models import World
from dnd_map.forms import ItemForm, CoordForm
from dnd_map.models import Item, Coord
from dnd_map.views.functions import calculate_depth, has_loop, check_leaf_depth


@login_required(login_url='dnd_imh:login')
def toggle_description(request, world_pk, item_pk):
    item = get_object_or_404(Item, pk=item_pk, world=get_object_or_404(World, pk=world_pk))

    if request.method == 'POST':
        item.show_description = request.POST['value'] == 'true'
        item.save()
        return HttpResponse(status=204)

    item.show_description = not item.show_description
    item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='dnd_imh:login')
def toggle_discovered(request, world_pk, item_pk):
    item = get_object_or_404(Item, pk=item_pk, world=get_object_or_404(World, pk=world_pk))

    if request.method == 'POST':
        if request.POST['value'] == 'true':
            item.set_discovered()
        else:
            item.set_undiscovered()

        return HttpResponse(status=204)

    if item.discovered:
        item.set_undiscovered()
    else:
        item.set_discovered()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='dnd_imh:login')
def new(request, world_pk, item_pk=0):
    world = get_object_or_404(World, pk=world_pk)

    context = {
        'world': world,
        'type': 'item',
        'edit': False,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            depth = calculate_depth(form.instance)

            if depth >= world.max_item_tree_depth:
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s depth would be bigger than the allowed maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)

            if depth < world.max_item_tree_depth:
                result = form.save(commit=False)
                result.depth = depth
                result.save()

            return HttpResponseRedirect(request.POST['return'])
        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        form = ItemForm(instance=Item(world=world))

        if item_pk != 0:
            parent = get_object_or_404(Item, pk=item_pk)
            if parent.depth < world.max_item_tree_depth - 1:
                form = ItemForm(instance=Item(parent=parent, world=world))

        form.fields['parent'].queryset = Item.objects.filter(world=world).exclude(depth=world.max_item_tree_depth - 1)
        form.fields['world'].queryset = World.objects.filter(pk=world_pk)

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='dnd_imh:login')
def new_coord(request, world_pk, item_pk):
    world = get_object_or_404(World, pk=world_pk)

    context = {
        'world': world,
        'type': 'coord',
        'edit': False,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = CoordForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.POST['return'])
        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        item = get_object_or_404(Item, pk=item_pk, world=world)
        form = CoordForm(instance=Coord(item=item, z_axis=item.depth))

        form.fields['item'].queryset = Item.objects.filter(world=world)
        form.fields['location'].queryset = Item.objects.filter(world=world).exclude(map='')

        maps = {}
        for item in form.fields['location'].queryset:
            img = Image.open(item.map.path)
            maps.update({
                item.pk: {
                    'url': item.map.url,
                    'width': img.width,
                    'height': img.height,
                }
            })
            img.close()

        img = Image.open(world.main_map)
        maps.update({
            '': {
                'url': world.main_map.url,
                'width': img.width,
                'height': img.height,
            },
        })
        img.close()

        context['form'] = form
        context['maps'] = json.dumps(maps)
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='dnd_imh:login')
def edit(request, world_pk, item_pk):
    world = get_object_or_404(World, pk=world_pk)
    item = get_object_or_404(Item, pk=item_pk)

    context = {
        'world': world,
        'type': 'item',
        'edit': True,
        'has_map': bool(item.map),
        'object': item,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            depth = calculate_depth(form.instance)

            # TODO: move to form's clean method
            if has_loop(form.instance):
                context.update({
                    'form': form,
                    'error': 'You selected a child as parent!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)
            if depth >= world.max_item_tree_depth:
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s depth would be bigger than the allowed maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)
            if not check_leaf_depth(form.instance, depth, world.max_item_tree_depth):
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s children\'s depth would be bigger than the allowed '
                             'maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)

            if calculate_depth(form.instance) < world.max_item_tree_depth:
                if request.POST['path'] != '':
                    if bool(form.instance.map):
                        if request.POST['path'] != form.instance.map.path:
                            os.remove(request.POST['path'])
                        else:
                            os.remove(request.POST['path'])

                result = form.save(commit=False)
                result.depth = depth
                result.save()

            return HttpResponseRedirect(request.POST['return'])

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        form = ItemForm(instance=item)

        form.fields['parent'].queryset = Item.objects.filter(world=world)\
                                                     .exclude(pk=item_pk)\
                                                     .exclude(depth=world.max_item_tree_depth - 1)

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='dnd_imh:login')
def edit_coord(request, world_pk, coord_pk):
    world = get_object_or_404(World, pk=world_pk)
    coord = get_object_or_404(Coord, pk=coord_pk)

    context = {
        'world': world,
        'type': 'coord',
        'edit': True,
        'has_map': False,
        'object': coord,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = CoordForm(request.POST, request.FILES, instance=coord)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.POST['return'])
        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        form = CoordForm(instance=get_object_or_404(Coord, pk=coord_pk))

        form.fields['item'].queryset = Item.objects.filter(world=world)
        form.fields['location'].queryset = Item.objects.filter(world=world).exclude(map='')

        maps = {}
        for item in form.fields['location'].queryset:
            img = Image.open(item.map.path)
            maps.update({
                item.pk: {
                    'url': item.map.url,
                    'width': img.width,
                    'height': img.height,
                }
            })
            img.close()

        img = Image.open(world.main_map)
        maps.update({
            '': {
                'url': world.main_map.url,
                'width': img.width,
                'height': img.height,
            },
        })
        img.close()

        context['form'] = form
        context['maps'] = json.dumps(maps)
        return render(request, 'dnd_map/admin/editor.html', context)


def remove(request, world_pk, object_type, object_pk, redirect):
    if object_type == 'item':
        obj = get_object_or_404(Item, pk=object_pk, world=get_object_or_404(World, pk=world_pk))

        if bool(obj.map):
            os.remove(obj.map.path)

        obj.delete()
    else:
        get_object_or_404(Coord, pk=object_pk).delete()

    return HttpResponseRedirect(redirect)
