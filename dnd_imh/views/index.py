from django.shortcuts import render


def index(request):
    return render(request, 'dnd_imh/index/index.html')
