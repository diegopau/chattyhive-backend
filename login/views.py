__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:  # Checking correct password written twice
                # Checking already existing user
                try:
                    if ChUser.objects.get(username=username) is not None:
                        return HttpResponse("Username already exists. Please, choose other")
                except ObjectDoesNotExist:
                    manager = ChUserManager()
                    user = manager.create_user(username, email, password)
            else:
                return HttpResponse("Password doesn't match")

            # Let's try to create a linked profile here
            profile = ChProfile(user=user)
            profile.save()

            # Let's try to save the user in a cookie
            request.session['user'] = profile.user.username
            request.session['pass'] = password

            return HttpResponseRedirect("/create_user/register1/")

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        return render(request, "login/create_user.html", {
            'form': form,
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        })
        # return render(request, "login/registration.html", {  # fixme only for test, use the lines above
        #     'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        # })


def register_one(request):
    if request.method == 'POST':
        user = request.session['user']
        prueba = ChProfile.objects.all()
        print(user)
        print(prueba)
        # profile = ChProfile.objects.get(user=request.user_pk=2)
        profile = ChProfile.objects.get(user__username=user)
        form = RegistrationFormOne(request.POST, instance=profile)
        if form.is_valid():
            print('form is valid')
            form.save()
            return HttpResponseRedirect("/create_user/register2/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = RegistrationFormOne()
        return render(request, "login/registration_1.html", {
            'form': form
        })
        # return HttpResponse("ERROR, invalid form 2")


def register_two(request):
    if request.method == 'POST':
        user = request.session['user']
        profile = ChProfile.objects.get(user__username=user)
        form = RegistrationFormTwo(request.POST, instance=profile)
        if form.is_valid():
            print('form is valid')
            form.save()

            # Trying login
            username = user
            print(username)
            password = request.session['pass']
            print(password)
            user2 = authenticate(username=username, password=password)
            if user2 is not None:
                if user2.is_active:
                    login(request, user2)
                    print("Login successful")
                    return HttpResponseRedirect("/chat/")
                else:
                    return HttpResponse("ERROR, inactive user")

            return HttpResponseRedirect("/chat/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = RegistrationFormTwo()
        return render(request, "login/registration_2.html", {
            'form': form
        })


def logout_view(request):
    print("logout")
    logout(request)
    request.session['active'] = False
    return HttpResponse("logged out")