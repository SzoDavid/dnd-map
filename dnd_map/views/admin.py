from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from dnd_map.models import Kingdom, City, Place


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))


@login_required(login_url='/dnd/login/')
def toggle_discovered(request, settlement_type, settlement_id):
    if settlement_type == 'kingdom':
        settlement_object = get_object_or_404(Kingdom, pk=settlement_id)
    elif settlement_type == 'city':
        settlement_object = get_object_or_404(City, pk=settlement_id)
    elif settlement_type == 'place':
        settlement_object = get_object_or_404(Place, pk=settlement_id)
    else:
        raise Http404("Type does not exist")

    settlement_object.discovered = not settlement_object.discovered

    if settlement_object.discovered:
        if settlement_type == 'city':
            settlement_object.kingdom.discovered = True
            settlement_object.kingdom.save()
        elif settlement_type == 'place':
            settlement_object.city.discovered = True
            settlement_object.city.kingdom.discovered = True
            settlement_object.city.save()
            settlement_object.city.kingdom.save()
    else:
        if settlement_type == 'kingdom':
            for city in settlement_object.city_set.filter(discovered=True):
                city.discovered = False
                city.save()
                for place in city.place_set.filter(discovered=True):
                    place.discovered = False
                    place.save()
        elif settlement_type == 'city':
            for place in settlement_object.place_set.filter(discovered=True):
                place.discovered = False
                place.save()

    settlement_object.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/dnd/login/')
def new(request, settlement_type):
    return new_parent(request, settlement_type, -1)


@login_required(login_url='/dnd/login/')
def new_parent(request, settlement_type, parent_id):
    kingdoms = None
    cities = None

    if settlement_type == 'city':
        kingdoms = Kingdom.objects.all()
    elif settlement_type == 'place':
        cities = City.objects.all()

    context = {
        'settlement_type': settlement_type,
        'kingdoms': kingdoms,
        'cities': cities,
        'return': request.META.get('HTTP_REFERER', '/'),
        'parent': parent_id,
    }

    return render(request, 'dnd_map/admin/new.html', context)


@login_required(login_url='/dnd/login/')
def edit(request, settlement_type, settlement_id):
    kingdoms = None
    cities = None

    if settlement_type == 'city':
        settlement = get_object_or_404(City, pk=settlement_id)
        kingdoms = Kingdom.objects.all()
    elif settlement_type == 'place':
        settlement = get_object_or_404(Place, pk=settlement_id)
        cities = City.objects.all()
    else:
        settlement = get_object_or_404(Kingdom, pk=settlement_id)

    context = {
        'settlement_type': settlement_type,
        'settlement': settlement,
        'kingdoms': kingdoms,
        'cities': cities,
        'return': request.META.get('HTTP_REFERER', '/'),
    }

    return render(request, 'dnd_map/admin/edit.html', context)


@login_required(login_url='/dnd/login/')
def update_db(request):

    if request.POST['map'].strip() == '':
        map_path = None
    else:
        map_path = request.POST['map'].strip()

    if request.POST['mode'] == 'new':
        if request.POST['settlement_type'] == 'kingdom':
            Kingdom(
                name=request.POST['name'].strip(),
                pronunciation=request.POST['pronunciation'].strip(),
                description=request.POST['description'].strip(),
                map__url=map_path,
                coords=request.POST['coords'].strip(),
                discovered='discovered' in request.POST
            ).save()
        elif request.POST['settlement_type'] == 'city':
            City(
                name=request.POST['name'].strip(),
                pronunciation=request.POST['pronunciation'].strip(),
                kingdom=Kingdom.objects.get(pk=request.POST['kingdom']),
                type=request.POST['type'].strip(),
                description=request.POST['description'].strip(),
                map__url=map_path,
                coords=request.POST['coords'].strip(),
                discovered='discovered' in request.POST,
                capital='capital' in request.POST
            ).save()
        else:
            Place(
                name=request.POST['name'].strip(),
                pronunciation=request.POST['pronunciation'].strip(),
                city=City.objects.get(pk=request.POST['city']),
                type=request.POST['type'].strip(),
                description=request.POST['description'].strip(),
                map__url=map_path,
                coords=request.POST['coords'].strip(),
                discovered='discovered' in request.POST
            ).save()
    else:
        if request.POST['settlement_type'] == 'kingdom':
            settlement = get_object_or_404(Kingdom, pk=request.POST['pk'])
        elif request.POST['settlement_type'] == 'city':
            settlement = get_object_or_404(City, pk=request.POST['pk'])
            settlement.kingdom = Kingdom.objects.get(pk=request.POST['kingdom'])
            settlement.type = request.POST['type'].strip()
            settlement.capital = 'capital' in request.POST
        else:
            settlement = get_object_or_404(Place, pk=request.POST['pk'])
            settlement.city = City.objects.get(pk=request.POST['city'])
            settlement.type = request.POST['type'].strip()

        settlement.name = request.POST['name'].strip()
        settlement.pronunciation = request.POST['pronunciation'].strip()
        settlement.description = request.POST['description'].strip()
        settlement.map = map_path
        settlement.coords = request.POST['coords'].strip()
        settlement.discovered = 'discovered' in request.POST
        settlement.save()

    return HttpResponseRedirect(request.POST['return'])


@login_required(login_url='/dnd/login/')
def remove(request, settlement_type, settlement_id, redirect):
    if settlement_type == 'kingdom':
        settlement = get_object_or_404(Kingdom, pk=settlement_id)
    elif settlement_type == 'city':
        settlement = get_object_or_404(City, pk=settlement_id)
    else:
        settlement = get_object_or_404(Place, pk=settlement_id)

    settlement.delete()

    return HttpResponseRedirect(redirect)
