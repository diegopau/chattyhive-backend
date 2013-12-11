__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from login.models import *
from django.contrib.auth import authenticate, login, logout
# from core.models import ChUserManager


def login_view(request):
    if request.method == 'POST':
        print("if")
        form = LoginForm(request.POST)
        if form.is_valid():
            # request.session['user'] = form.cleaned_data['user']
            # request.session['active'] = True
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            # request.session.set_expiry(300)
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
        # print("21 /b",request.session['active'])
        # if 'user' in request.session and request.session['active']==True:
        #     print('one')
        #     request.session.set_expiry(300)
        #     return HttpResponseRedirect("/chat/")
        # else:
        form = LoginForm()
        print('two')
        return render(request, "login/login.html", {
            'form': form
        })

def create_user_view(request):
    if request.method == 'POST':
        print("if")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            manager = ChUserManager()
            manager.create_user(manager, username, "", password) #TODO not working yet, says 5 arguments given

            # request.session.set_expiry(300)
            user2 = authenticate(username=username, password=password)
            if user2 is not None:
                if user2.is_active:
                    login(request, user2)
                    return HttpResponseRedirect("/chat/")
                else:
                    return HttpResponse("ERROR, inactive user")
            # else:
            #     return HttpResponse("ERROR, incorrect password or login")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        return render(request, "login/create_user.html", {
            'form': form
        })

def logout_view(request):
    print("logout")
    logout(request)
    # print("11 /b",request.session['active'])
    request.session['active'] = False
    # print("12 /b",request.session['active'])
    return HttpResponse("logged out")