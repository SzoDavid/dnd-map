import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
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
            'settlement_type': 'item',
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
            'settlement_type': 'coord',
            'return': request.META.get('HTTP_REFERER', '/')}

        return render(request, 'dnd_map/admin/new.html', context)


@login_required(login_url='/dnd/login/')
def edit(request, settlement_type, settlement_id):
    # if settlement_type == 'kingdom':
    #     settlement = get_object_or_404(Kingdom, pk=settlement_id)
    # elif settlement_type == 'city':
    #     settlement = get_object_or_404(City, pk=settlement_id)
    # elif settlement_type == 'place':
    #     settlement = get_object_or_404(Place, pk=settlement_id)
    # elif settlement_type == 'terrain':
    #     settlement = get_object_or_404(Terrain, pk=settlement_id)
    # else:
    #     settlement = get_object_or_404(TerrainCoords, pk=settlement_id)
    #
    # if request.method == 'POST':
    #     if settlement_type == 'kingdom':
    #         form = KingdomForm(request.POST, request.FILES, instance=settlement)
    #     elif settlement_type == 'city':
    #         form = CityForm(request.POST, request.FILES, instance=settlement)
    #     elif settlement_type == 'place':
    #         form = PlaceForm(request.POST, request.FILES, instance=settlement)
    #     elif settlement_type == 'terrain':
    #         form = TerrainForm(request.POST, instance=settlement)
    #     else:
    #         form = TerrainCoordsForm(request.POST, instance=settlement)
    #
    #     if form.is_valid():
    #         if request.POST['path'] != '':
    #             if bool(form.instance.map):
    #                 if request.POST['path'] != form.instance.map.path:
    #                     os.remove(request.POST['path'])
    #             else:
    #                 os.remove(request.POST['path'])
    #
    #         form.save()
    #
    #         return HttpResponseRedirect(request.POST['return'])
    # else:
    #     if settlement_type == 'kingdom':
    #         form = KingdomForm(instance=settlement)
    #     elif settlement_type == 'city':
    #         form = CityForm(instance=settlement)
    #     elif settlement_type == 'place':
    #         form = PlaceForm(instance=settlement)
    #     elif settlement_type == 'terrain':
    #         form = TerrainForm(instance=settlement)
    #     else:
    #         form = TerrainCoordsForm(instance=settlement)
    #
    #     settlement_has_map = False
    #
    #     if not (settlement_type == 'terrain' or settlement_type == 'terrain_coords'):
    #         settlement_has_map = bool(settlement.map)
    #
    #     if settlement_type == 'terrain_coords':
    #         settlement_type = 'coords'
    #
    #     context = {
    #         'form': form,
    #         'settlement_type': settlement_type,
    #         'settlement_has_map': settlement_has_map,
    #         'settlement': settlement,
    #         'return': request.META.get('HTTP_REFERER', '/')}
    #
    #     return render(request, 'dnd_map/admin/edit.html', context)
    return


@login_required(login_url='/dnd/login/')
def edit_coord(request, settlement_type, settlement_id):
    return


@login_required(login_url='/dnd/login/')
def remove(request, object_type, object_pk, redirect):
    if object_type == 'item':
        get_object_or_404(Item, pk=object_pk).delete()
    else:
        get_object_or_404(Coord, pk=object_pk).delete()

    return HttpResponseRedirect(redirect)
