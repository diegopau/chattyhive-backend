__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from social.backends.google import GooglePlusAuth


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/chat/")
                else:
                    return HttpResponse("ERROR, inactive user")
            else:
                return HttpResponse("ERROR, incorrect password or login")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = LoginForm()
        return render(request, "login/login.html", {
            'form': form
        })

def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            manager = ChUserManager()
            manager.create_user(manager, username, "", password) #TODO not working yet, says 5 arguments given

            user2 = authenticate(username=username, password=password)
            if user2 is not None:
                if user2.is_active:
                    login(request, user2)
                    return HttpResponseRedirect("/chat/")
                else:
                    return HttpResponse("ERROR, inactive user")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        # return render(request, "login/create_user.html", {
        #     'form': form
        # })
        return render(request, "login/registration.html", { #fixme only for test, use the lines above
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        })

def logout_view(request):
    print("logout")
    logout(request)
    request.session['active'] = False
    return HttpResponse("logged out")