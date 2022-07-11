from django.db.models import Q
from django.shortcuts import render

from dnd_imh.models import World


def worlds(request):
    context = {}

    if request.method == 'POST':
        search_value = request.POST['search']
        context['search'] = search_value
        context['worlds'] = World.objects.filter(Q(name__icontains=search_value) | Q(owner__username__icontains=search_value))
    else:
        context['worlds'] = World.objects.all()

    return render(request, 'dnd_imh/worlds/worlds.html', context)
