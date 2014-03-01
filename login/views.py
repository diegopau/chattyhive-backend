__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from social.backends.google import GooglePlusAuth
from django.contrib.auth.decorators import login_required
from social.apps.django_app.default.models import UserSocialAuth
from uuid import uuid4


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
            email = form.cleaned_data['email']
            username = email  # TODO temporal solution, should be changed
            password = uuid4().hex

            # Checking already existing user
            try:
                if ChUser.objects.get(username=username) is not None:
                    return HttpResponse("Username already exists. Please, choose other")
            except ObjectDoesNotExist:
                manager = ChUserManager()
                user = manager.create_user(username, email, password)

            # Let's try to create a linked profile here
            profile = ChProfile(user=user)
            profile.save()

            user2 = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user2)
                else:
                    return HttpResponse("ERROR, inactive user")
            else:
                return HttpResponse("UNKNOWN ERROR")

            return HttpResponseRedirect("/create_user/register1/")

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        return render(request, "login/registration.html", {
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
            'plus_scope' : ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
            'form': form
        })


@login_required
def register_one(request):
    if request.method == 'POST':
        user = request.user
        profile = ChProfile.objects.get(user=user)

        form = RegistrationFormOne(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/create_user/register2/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        profile = ChProfile.objects.get(user__username=request.user)
        form = RegistrationFormOne(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'sex': profile.sex,
            'language': profile.language,
            'private_show_age': profile.private_show_age,
            'location': profile.location,
        })
        return render(request, "login/registration_1.html", {
            'form': form
        })


@login_required
def register_two(request):
    if request.method == 'POST':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        form = RegistrationFormTwo(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/create_user/register3/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        profile = ChProfile.objects.get(user__username=request.user)
        form = RegistrationFormTwo(initial={
            'public_name': profile.public_name,
            'public_show_age': profile.public_show_age,
            'show_location': profile.show_location,
        })
        return render(request, "login/registration_2.html", {
            'form': form
        })


@login_required
def register_three(request):
    if request.method == 'POST':
        user = request.user
        form = RegistrationFormThree(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email  # TODO temporal solution, should be changed
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:  # Checking correct password written twice
                user.username = username
                user.set_password(password)
                user.save()
            else:
                return HttpResponse("Passwords don't match")

            return HttpResponseRedirect("/home/")

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        try:
            user_social = UserSocialAuth.objects.get(user=request.user)
            if user_social.provider == 'twitter':
                form = RegistrationFormThree()
            else:
                form = RegistrationFormThree(initial={
                    'email': request.user.username,
                })
        except UserSocialAuth.DoesNotExist:
            form = RegistrationFormThree(initial={
                'email': request.user.username,
            })
        return render(request, "login/create_user.html", {
            'form': form,
        })


def logout_view(request):
    logout(request)
    request.session['active'] = False
    return HttpResponse("logged out")