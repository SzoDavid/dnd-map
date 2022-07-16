from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from dnd_imh.models import World, Backup
from dnd_map.models import Item, Coord


@login_required(login_url='dnd_imh:login')
def export(request, world_pk):
    world = get_object_or_404(World, pk=world_pk)
    items = serializers.serialize("json", Item.objects.filter(world=world))
    coords = serializers.serialize("json", Coord.objects.filter(item__world=world))

    json = '{"world": ' + serializers.serialize("json", World.objects.filter(pk=world_pk)) + '. "items": '
    if items:
        json += items + ', "coords": '
    else:
        json += '[], "coords": '
    json += ''
    if coords:
        json += coords + '}'
    else:
        json += '[]}'

    backup = Backup(name=world.name, owner=world.owner, created=timezone.now(), data=json)
    backup.save()

    return redirect(reverse('dnd_imh:user', args=[request.user.pk, ]))
