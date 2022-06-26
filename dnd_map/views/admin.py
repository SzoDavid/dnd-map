from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return HttpResponseRedirect(reverse('dnd_map:index'))
#     else:
#         return HttpResponseRedirect(reverse('dnd_map:login'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('dnd_map:index'))
