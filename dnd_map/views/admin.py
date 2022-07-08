import json
import os

from PIL import Image
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from dnd_map.forms import ItemForm, CoordForm
from dnd_map.models import Item, Coord
from dnd_map.views.functions import calculate_depth, has_loop, check_leaf_depth

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))


@login_required(login_url='/dnd/login/')
def toggle_description(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if request.method == 'POST':
        item.show_description = request.POST['value'] == 'true'
        item.save()
        return HttpResponse(status=204)

    item.show_description = not item.show_description
    item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/dnd/login/')
def toggle_discovered(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

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


@login_required(login_url='/dnd/login/')
def new(request, item_pk=0):
    config = json.load(open(SITE_ROOT + '/../config.json'))

    context = {
        'type': 'item',
        'edit': False,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            depth = calculate_depth(form.instance)

            if depth >= config['max_item_display_depth']:
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s depth would be bigger than the allowed maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)

            if depth < config['max_item_display_depth']:
                result = form.save(commit=False)
                result.depth = depth
                result.save()

            return HttpResponseRedirect(request.POST['return'])
        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        form = ItemForm()

        if item_pk != 0:
            parent = get_object_or_404(Item, pk=item_pk)
            if parent.depth < config['max_item_display_depth'] - 1:
                form = ItemForm(instance=Item(parent=parent))

        form.fields['parent'].queryset = Item.objects.exclude(depth=config['max_item_display_depth'] - 1)

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='/dnd/login/')
def new_coord(request, item_pk):
    context = {
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
        config = json.load(open(SITE_ROOT + '/../config.json'))

        item = get_object_or_404(Item, pk=item_pk)
        form = CoordForm(instance=Coord(item=item, z_axis=item.depth))

        form.fields['location'].queryset = Item.objects.exclude(map='')

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

        img = Image.open(SITE_ROOT + '/../static/dnd_map/images/maps/' + config['main_map']['path'])
        maps.update({
            '': {
                'url': '/static/dnd_map/images/maps/' + config['main_map']['path'],
                'width': img.width,
                'height': img.height,
            },
        })
        img.close()

        context['form'] = form
        context['maps'] = json.dumps(maps)
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='/dnd/login/')
def edit(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    config = json.load(open(SITE_ROOT + '/../config.json'))

    context = {
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
            if depth >= config['max_item_display_depth']:
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s depth would be bigger than the allowed maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)
            if not check_leaf_depth(form.instance, depth, config['max_item_display_depth']):
                context.update({
                    'form': form,
                    'error': 'By selecting that parent the item\'s children\'s depth would be bigger than the allowed '
                             'maximum!'
                })
                return render(request, 'dnd_map/admin/editor.html', context)

            if calculate_depth(form.instance) < config['max_item_display_depth']:
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

        form.fields['parent'].queryset = Item.objects.exclude(pk=item_pk)\
                                                     .exclude(depth=config['max_item_display_depth'] - 1)

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='/dnd/login/')
def edit_coord(request, coord_pk):
    coord = get_object_or_404(Coord, pk=coord_pk)

    context = {
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
        config = json.load(open(SITE_ROOT + '/../config.json'))

        form = CoordForm(instance=get_object_or_404(Coord, pk=coord_pk))

        form.fields['location'].queryset = Item.objects.exclude(map='')

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

        img = Image.open(SITE_ROOT + '/../static/dnd_map/images/maps/' + config['main_map']['path'])
        maps.update({
            '': {
                'url': '/static/dnd_map/images/maps/' + config['main_map']['path'],
                'width': img.width,
                'height': img.height,
            },
        })
        img.close()

        context['form'] = form
        context['maps'] = json.dumps(maps)
        return render(request, 'dnd_map/admin/editor.html', context)


def remove(request, object_type, object_pk, redirect):
    if object_type == 'item':
        obj = get_object_or_404(Item, pk=object_pk)

        if bool(obj.map):
            os.remove(obj.map.path)

        obj.delete()
    else:
        get_object_or_404(Coord, pk=object_pk).delete()

    return HttpResponseRedirect(redirect)
