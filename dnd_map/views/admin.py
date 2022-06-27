from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from dnd_map.models import Kingdom, City, Place


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))


@login_required(login_url='/dnd/login/')
def switch_discovered(request, settlement_type, settlement_id):
    if settlement_type == 'kingdom':
        settlement_object = get_object_or_404(Kingdom, pk=settlement_id)
    elif settlement_type == 'city':
        settlement_object = get_object_or_404(City, pk=settlement_id)
    elif settlement_type == 'place':
        settlement_object = get_object_or_404(Place, pk=settlement_id)
    else:
        raise Http404("Type does not exist")

    settlement_object.discovered = not settlement_object.discovered
    settlement_object.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

