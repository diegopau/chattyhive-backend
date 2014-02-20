__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from social.backends.google import GooglePlusAuth


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/home/")
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
            # username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            username = email  # TODO temporal solution, should be changed
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
            request.session['email'] = profile.user.username
            request.session['pass'] = password

            return HttpResponseRedirect("/create_user/register1/")

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        # return render(request, "login/create_user.html", {
        #     'form': form,
        #     'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        # })
        return render(request, "login/registration.html", {  # FIXME only for test, use the lines above
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
            'plus_scope' : ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
        })


def register_one(request):
    if request.method == 'POST': # todo if authenticated
        user = request.session['email']
        # ===============================
        prueba = ChProfile.objects.all()
        print(user)
        print(prueba)
        # ===============================
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
        if request.user.is_authenticated():
            print(request.user)
            profile = ChProfile.objects.get(user__username=request.user)
            # form.fields['first_name'].cleaned_data = profile.first_name
            form = RegistrationFormOne(initial={
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'sex': profile.sex,
                'language': profile.language,
                'private_show_age': profile.private_show_age,
                'location': profile.location,
            })
        else:
            form = RegistrationFormOne()
        return render(request, "login/registration_1.html", {
            'form': form
        })
        # return HttpResponse("ERROR, invalid form 2")


def register_two(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            user = request.user
        else:
            user = request.session['email']
        profile = ChProfile.objects.get(user__username=user)
        form = RegistrationFormTwo(request.POST, instance=profile)
        if form.is_valid():
            print('form is valid')
            form.save()

            if request.user.is_authenticated():
                return HttpResponseRedirect("/home/")

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
                    return HttpResponseRedirect("/home/")
                else:
                    return HttpResponse("ERROR, inactive user")

            return HttpResponseRedirect("/home/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        if request.user.is_authenticated():
            print(request.user)
            profile = ChProfile.objects.get(user__username=request.user)
            form = RegistrationFormTwo(initial={
                'public_name': profile.public_name,
                'public_show_age': profile.public_show_age,
                'show_location': profile.show_location,
            })
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