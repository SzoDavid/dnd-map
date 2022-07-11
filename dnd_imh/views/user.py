import os

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from dnd_imh.forms import WorldForm, RegisterForm
from dnd_imh.models import World
from dnd_map.models import Item


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect(reverse('dnd_imh:index'))
        context['form'] = form
        return render(request, 'dnd_imh/user/register.html', context)
    else:
        form = RegisterForm()
        context['form'] = form
        return render(request, 'dnd_imh/user/register.html', context)


@login_required(login_url='dnd_imh:login')
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


@login_required(login_url='dnd_imh:login')
def edit_world(request, world_pk):
    world = get_object_or_404(World, pk=world_pk)

    if request.user != world.owner:
        return redirect(reverse('dnd_imh:index'))

    context = {
        'world': world,
        'edit': True,
        'has_map': bool(world.main_map),
        'return': request.META.get('HTTP_REFERER', '/')}

    if request.method == 'POST':
        form = WorldForm(request.POST, request.FILES, instance=world)

        if form.is_valid():
            if request.POST['path'] != '':
                if bool(form.instance.main_map):
                    if request.POST['path'] != form.instance.main_map.path:
                        os.remove(request.POST['path'])
                    else:
                        os.remove(request.POST['path'])

            form.save()

            return HttpResponseRedirect(request.POST['return'])

        context['form'] = form
        return render(request, 'dnd_imh/user/editor.html', context)
    else:
        form = WorldForm(instance=world)

        context['form'] = form
        return render(request, 'dnd_imh/user/editor.html', context)


@login_required(login_url='dnd_imh:login')
def remove_world(request, world_pk):
    world = get_object_or_404(World, pk=world_pk)

    if request.user != world.owner:
        return redirect(reverse('dnd:imh:index'))

    if bool(world.main_map):
        os.remove(world.main_map.path)

    for item in Item.objects.filter(world=world):
        if bool(item.map):
            os.remove(item.map.path)

    world.delete()

    return redirect(reverse('dnd_imh:index'))
