import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# from dnd_map.forms import KingdomForm, CityForm, PlaceForm, TerrainForm, TerrainCoordsForm
# from dnd_map.models import Kingdom, City, Place, TerrainCoords, Terrain


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))


@login_required(login_url='/dnd/login/')
def toggle_discovered(request, settlement_type, settlement_id):
    # if settlement_type == 'kingdom':
    #     settlement_object = get_object_or_404(Kingdom, pk=settlement_id)
    # elif settlement_type == 'city':
    #     settlement_object = get_object_or_404(City, pk=settlement_id)
    # elif settlement_type == 'place':
    #     settlement_object = get_object_or_404(Place, pk=settlement_id)
    # elif settlement_type == 'terrain':
    #     settlement_object = get_object_or_404(Terrain, pk=settlement_id)
    # else:
    #     raise Http404("Type does not exist")
    #
    # if settlement_type == 'terrain':
    #     settlement_object.show_description = not settlement_object.show_description
    # else:
    #     settlement_object.discovered = not settlement_object.discovered
    #
    #     if settlement_object.discovered:
    #         if settlement_type == 'city':
    #             settlement_object.kingdom.discovered = True
    #             settlement_object.kingdom.save()
    #         elif settlement_type == 'place':
    #             settlement_object.city.discovered = True
    #             settlement_object.city.kingdom.discovered = True
    #             settlement_object.city.save()
    #             settlement_object.city.kingdom.save()
    #     else:
    #         if settlement_type == 'kingdom':
    #             for city in settlement_object.city_set.filter(discovered=True):
    #                 city.discovered = False
    #                 city.save()
    #                 for place in city.place_set.filter(discovered=True):
    #                     place.discovered = False
    #                     place.save()
    #         elif settlement_type == 'city':
    #             for place in settlement_object.place_set.filter(discovered=True):
    #                 place.discovered = False
    #                 place.save()
    #
    # settlement_object.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/dnd/login/')
def new(request, settlement_type, parent_id=0):
    # if request.method == 'POST':
    #     if settlement_type == 'kingdom':
    #         form = KingdomForm(request.POST, request.FILES)
    #     elif settlement_type == 'city':
    #         form = CityForm(request.POST, request.FILES)
    #     elif settlement_type == 'place':
    #         form = PlaceForm(request.POST, request.FILES)
    #     elif settlement_type == 'terrain':
    #         form = TerrainForm(request.POST)
    #     else:
    #         form = TerrainCoordsForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #
    #         return HttpResponseRedirect(request.POST['return'])
    # else:
    #     if settlement_type == 'kingdom':
    #         form = KingdomForm()
    #     elif settlement_type == 'city':
    #         form = CityForm(instance=City(kingdom=get_object_or_404(Kingdom, pk=parent_id)))
    #     elif settlement_type == 'place':
    #         form = PlaceForm(instance=Place(city=get_object_or_404(City, pk=parent_id)))
    #     elif settlement_type == 'terrain':
    #         form = TerrainForm()
    #     else:
    #         form = TerrainCoordsForm(instance=TerrainCoords(terrain=get_object_or_404(Terrain, pk=parent_id)))
    #
    #     if settlement_type == 'terrain_coords':
    #         settlement_type = 'coords'
    #
    #     context = {
    #         'form': form,
    #         'settlement_type': settlement_type,
    #         'return': request.META.get('HTTP_REFERER', '/')}
    #
    #     return render(request, 'dnd_map/admin/new.html', context)
    return


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
def remove(request, settlement_type, settlement_id, redirect):
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
    # settlement.delete()

    return HttpResponseRedirect(redirect)
