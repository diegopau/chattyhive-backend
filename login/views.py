# -*- encoding: utf-8 -*-
from email_confirmation.models import EmailAddress, EmailConfirmation

__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from login.models import *
from CH import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from social.backends.google import GooglePlusAuth
from social.apps.django_app.default.models import UserSocialAuth
from uuid import uuid4
import json
from django.core.serializers.json import DjangoJSONEncoder
import pusher
from django.db import IntegrityError
from django.forms.models import inlineformset_factory
from django.core.mail import send_mail
from email_confirmation import *


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                login_string = form.cleaned_data['login']
                password = form.cleaned_data['password']
                if '@' in login_string:
                    user = ChUser.objects.get(email=login_string)
                    user = authenticate(username=user.username, password=password)
                else:
                    profile = ChProfile.objects.select_related().get(public_name=login_string)
                    user = authenticate(username=profile.user.username, password=password)
                if user.is_active:
                    login(request, user)
                    email_address = EmailAddress.objects.get(email=user.email)
                    if not email_address.verified:
                        if EmailConfirmation.key_expired(EmailConfirmation.objects.get(
                                email_address=EmailAddress.objects.get(email=user.email))) and not email_address.warned:
                            EmailAddress.objects.warn(login_string)
                            return HttpResponseRedirect("/email_warning/")
                        if email_address.warned:
                            if EmailConfirmation.warning_expired(
                                    EmailConfirmation.objects.get(email_address=EmailAddress.objects.get(email=user.email))):
                                EmailAddress.objects.check_confirmation(login_string)
                            else:
                                return HttpResponseRedirect("/email_warning/")
                    return HttpResponseRedirect("/home/")
                else:
                    # user.delete()
                    # TODO set an html to resend confirmation
                    return HttpResponse("This account has been deleted due its email has not been confirmed."
                                        " Please register again")
            except ChUser.DoesNotExist or ChProfile.DoesNotExist:
                return HttpResponse("ERROR, incorrect password or login")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = LoginForm()
        return render(request, "login/login.html", {
            'form': form
        })


def create_user_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = uuid4().hex  # this password will be used until the user enter a new one
                manager = ChUserManager()
                user = manager.create_user('unused', email, password)

                # Profile creation
                original_name = re.sub('[.-]', '_', email.split('@')[0])  # '.' and '-' replaced by '_'
                original_name = re.sub('[^0-9a-zA-Z_]+', '', original_name)    # other not allowed characters eliminated
                public_name = original_name
                # if the name already exists we offer the name plus '_<number>'
                ii = 0
                while True:
                    try:
                        ChProfile.objects.get(public_name=public_name)
                    except ChProfile.DoesNotExist:
                        break
                    ii += 1
                    public_name = original_name + '_' + str(ii)

                profile = ChProfile(user=user, public_name=public_name)  # temporal profile name
                profile.save()

                user2 = authenticate(username=user.username, password=password)
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
    """

    :param request:
    :return:
    """
    user = request.user
    profile = ChProfile.objects.get(user=user)
    # language_formset = inlineformset_factory(ChProfile, LanguageModel, max_num=2)
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
            'private_show_age': profile.private_show_age,
            'country': profile.country,
            'region': profile.region,
            'city': profile.city,
            })
        return render(request, "login/registration_1.html", {
            'form': form,
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
            'show_location': profile.public_show_location,
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
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:  # Checking correct password written twice
                try:
                    # user.username = username
                    user.email = email
                    user.set_password(password)
                    user.save()

                    profile = ChProfile.objects.get(user=user)
                    EmailAddress.objects.add_email(user=profile, email=email)

                    profile = ChProfile.objects.get(user=user)
                    profile.set_private_status('I\'m new in chattyhive!')
                    profile.set_public_status('I\'m new in chattyhive!')

                    color = ''
                    for ii in range(3):
                        while True:
                            rgb = uuid4().hex[:2]
                            if 'EE' > rgb > '20':
                                break
                        color = color + rgb
                    profile.set_personal_color('#' + color)

                    profile.save()

                # if the email is already used
                except IntegrityError:
                    form = RegistrationFormThree()
                    return render(request, "login/create_user.html", {
                        'form': form,
                        'error': 'email',
                    })

            else:
                form = RegistrationFormThree()
                return render(request, "login/create_user.html", {
                    'form': form,
                    'error': 'password',
                })

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
                    'email': request.user.email,
                })
        except UserSocialAuth.DoesNotExist:
            form = RegistrationFormThree(initial={
                'email': request.user.email,
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