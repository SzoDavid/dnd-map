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
            settlement_object = get_object_or_404(City, pk=settlement_id)
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
        'mode': 'new',
        'return': request.META.get('HTTP_REFERER', '/'),
        'parent': parent_id,
    }

    return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='/dnd/login/')
def edit(request, settlement_type, settlement_id):
    return


@login_required(login_url='/dnd/login/')
def update_db(request):
    if request.POST['map_path'].strip() == '':
        map_path = None
    else:
        map_path = request.POST['map_path'].strip()

    if request.POST['mode'] == 'new':
        if request.POST['settlement_type'] == 'kingdom':
            Kingdom(
                name=request.POST['name'].strip(),
                pronunciation=request.POST['pronunciation'].strip(),
                description=request.POST['description'].strip(),
                map_path=map_path,
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
                map_path=map_path,
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
                map_path=map_path,
                coords=request.POST['coords'].strip(),
                discovered='discovered' in request.POST
            ).save()

    return HttpResponseRedirect(request.POST['return'])


@login_required(login_url='/dnd/login/')
def remove(request, settlement_id):
    return
