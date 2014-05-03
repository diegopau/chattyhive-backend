# -*- encoding: utf-8 -*-
from django.db import IntegrityError

__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from social.backends.google import GooglePlusAuth
from social.apps.django_app.default.models import UserSocialAuth
from uuid import uuid4
import json
from django.core.serializers.json import DjangoJSONEncoder
import pusher
from django.core.mail import send_mail
from email_confirmation import *


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
            try:
                email = form.cleaned_data['email']
                username = email        # TODO temporal solution, should be changed
                password = uuid4().hex  # this password will be used until the user enter a new one
                manager = ChUserManager()
                user = manager.create_user(username, email, password)

                # Profile creation
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

            # if the email is already used
            except IntegrityError:
                form = CreateUserForm()
                return render(request, "login/registration.html", {
                    'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                    'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
                    'form': form,
                    'error': 'email',
                })

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateUserForm()
        return render(request, "login/registration.html", {
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
            'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
            'form': form
        })


@login_required
def register_one(request):
    user = request.user
    profile = ChProfile.objects.get(user=user)
    if request.method == 'POST':

        form = RegistrationFormOne(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/create_user/register2/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
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
    user = request.user
    profile = ChProfile.objects.get(user=user)
    if request.method == 'POST':
        form = RegistrationFormTwo(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/create_user/register3/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
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
    user = request.user
    if request.method == 'POST':
        form = RegistrationFormThree(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email  # TODO temporal solution, should be changed
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:  # Checking correct password written twice
                try:
                    user.username = username
                    user.set_password(password)
                    user.save()

                    profile = ChProfile.objects.get(user=user)
                    # mail_manager = EmailAddressManager()
                    print(profile)  # PRINT
                    mail_address = EmailAddress.objects.add_email(user=profile, email=email)
                    # mail_address
                    # mail_address.user = profile
                    # mail_address.email = email
                    # mail_address.save()
                    # email_address.set_as_primary(conditional=True)
                    # email_address.save()

                    # Send confirmation email here
                    # send_mail(SUBJECT, MESSAGE, FROM_MAIL, TO_LIST, FAIL_SILENTLY)

                # if the email is already used
                except IntegrityError:
                    form = RegistrationFormThree()
                    return render(request, "login/create_user.html", {
                        'form': form,
                        'error': 'email',
                    })

            else:
                return HttpResponse("Passwords don't match")

            return HttpResponseRedirect("/home/")

        else:
            return HttpResponse("ERROR, invalid form")
    else:
        try:    # if the user is created by twitter a valid email must be provided
            user_social = UserSocialAuth.objects.get(user=user)
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
            'error': 'none',
        })


def logout_view(request):
    logout(request)
    request.session['active'] = False
    return HttpResponse("logged out")


@login_required
def chat_auth(request):
    user = request.user
    if request.method == 'POST':
        chat_channel = request.POST['channel_name']
        chat = ChChat.objects.get(channel_unicode=chat_channel)
        socket_id = request.POST['socket_id']

        profile = ChProfile.objects.get(user=user)
        hive = chat.hive

        try:
            ChSubscription.objects.get(hive=hive, profile=profile)

            channel_data = {'user_id': socket_id,
                            'user_info': {'public_name': profile.public_name,
                                          'username': user.username
                            }
            }

            app_key = "55129"
            key = 'f073ebb6f5d1b918e59e'
            secret = '360b346d88ee47d4c230'

            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret,
                encoder=DjangoJSONEncoder,
            )

            auth_response = p[chat_channel].authenticate(socket_id, channel_data)

            return HttpResponse(json.dumps(auth_response, cls=DjangoJSONEncoder))

        except ChSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response

    else:
        raise Http404