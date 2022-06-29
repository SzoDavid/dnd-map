import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from dnd_map.forms import ItemForm, CoordForm
from dnd_map.models import Item, Coord


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))


@login_required(login_url='/dnd/login/')
def toggle_description(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    item.show_description = not item.show_description
    item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/dnd/login/')
def toggle_discovered(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.discovered:
        item.set_undiscovered()
    else:
        item.set_discovered()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/dnd/login/')
def new(request, item_pk=0):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():

            # TODO: validate depth

            form.save()

            return HttpResponseRedirect(request.POST['return'])
    else:
        if item_pk == 0:
            form = ItemForm()
        else:
            parent = get_object_or_404(Item, pk=item_pk)
            form = ItemForm(instance=Item(parent=parent, depth=parent.depth + 1))

        context = {
            'form': form,
            'type': 'item',
            'return': request.META.get('HTTP_REFERER', '/')}

        return render(request, 'dnd_map/admin/new.html', context)


@login_required(login_url='/dnd/login/')
def new_coord(request, item_pk):
    if request.method == 'POST':
        form = CoordForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.POST['return'])
    else:
        item = get_object_or_404(Item, pk=item_pk)
        form = CoordForm(instance=Coord(item=item, z_axis=item.depth))

        context = {
            'form': form,
            'type': 'coord',
            'return': request.META.get('HTTP_REFERER', '/')}

        return render(request, 'dnd_map/admin/new.html', context)


@login_required(login_url='/dnd/login/')
def edit(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            if request.POST['path'] != '':
                if bool(form.instance.map):
                    if request.POST['path'] != form.instance.map.path:
                        os.remove(request.POST['path'])
                    else:
                        os.remove(request.POST['path'])

            # TODO: validate depth and check for loops

            form.save()

            return HttpResponseRedirect(request.POST['return'])
    else:
        form = ItemForm(instance=get_object_or_404(Item, pk=item_pk))

        context = {
            'form': form,
            'type': 'item',
            'has_map': bool(item.map),
            'object': item,
            'return': request.META.get('HTTP_REFERER', '/')}

        return render(request, 'dnd_map/admin/edit.html', context)


@login_required(login_url='/dnd/login/')
def edit_coord(request, coord_pk):
    coord = get_object_or_404(Coord, pk=coord_pk)
    if request.method == 'POST':
        form = CoordForm(request.POST, request.FILES, instance=coord)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.POST['return'])
    else:
        form = CoordForm(instance=get_object_or_404(Coord, pk=coord_pk))

        context = {
            'form': form,
            'type': 'coord',
            'has_map': False,
            'object': coord,
            'return': request.META.get('HTTP_REFERER', '/')}

        return render(request, 'dnd_map/admin/edit.html', context)


@login_required(login_url='/dnd/login/')
def remove(request, object_type, object_pk, redirect):
    if object_type == 'item':
        get_object_or_404(Item, pk=object_pk).delete()
    else:
        get_object_or_404(Coord, pk=object_pk).delete()

    return HttpResponseRedirect(redirect)
