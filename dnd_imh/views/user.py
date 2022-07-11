import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from dnd_imh.forms import WorldForm
from dnd_imh.models import World


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def create_world(request):
    context = {
        'edit': False,
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = WorldForm(request.POST, request.FILES)

        if form.is_valid():
            world = form.save()

            return redirect(reverse('dnd_map:index', args=(world.pk,)))
        context['form'] = form
        return render(request, 'dnd_imh/user/editor.html', context)
    else:
        form = WorldForm(instance=World(owner=request.user))
        context['form'] = form
        return render(request, 'dnd_imh/user/editor.html', context)


@login_required(login_url='/login/')
def edit_world(request, world_pk):
    world = get_object_or_404(World, pk=world_pk)

    if request.user != world.owner:
        return redirect(reverse('dnd:imh:index'))

    context = {
        'world': world,
        'edit': True,
        'has_map': bool(world.map),
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = WorldForm(request.POST, request.FILES, instance=world)

        if form.is_valid():
            if request.POST['path'] != '':
                if bool(form.instance.map):
                    if request.POST['path'] != form.instance.map.path:
                        os.remove(request.POST['path'])
                    else:
                        os.remove(request.POST['path'])

            form.save()

            return HttpResponseRedirect(request.POST['return'])

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)
    else:
        form = WorldForm(instance=world)

        context['form'] = form
        return render(request, 'dnd_map/admin/editor.html', context)


@login_required(login_url='/login/')
def remove_form(request, world_pk):
    return
