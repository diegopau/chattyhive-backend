# -*- encoding: utf-8 -*-
from core.models import MsgForm

__author__ = 'lorenzo'

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from django.contrib.auth.decorators import login_required
import pusher


@login_required
def create_hive(request):
    """
    :param request:
    :return: Web page with the form for creating a hive
    """
    if request.method == 'POST':
        form = CreateHiveForm(request.POST)
        if form.is_valid():
            print('form is valid')
            hive = form.cleaned_data['name']
            hive = hive.replace(" ", "_")
            form.cleaned_data['name'] = hive
            form.save()
            print(hive)
            request.session['hive'] = hive
            return HttpResponseRedirect("/create_hive/create/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateHiveForm()
        return render(request, "core/create_hive.html", {
            'form': form
        })


@login_required
def create_hive_created(request):
    """
    :param request:
    :return: Home web page after creating the hive
    """
    # Getting needed information
    username = request.user
    user = ChUser.objects.get(username=username)
    profile = ChProfile.objects.get(user=user)
    aux = profile.location
    print(aux)  # PRINT
    hive_name = request.session['hive']
    hive_name = hive_name.replace("_", " ")
    hive = ChHive.objects.get(name=hive_name)

    # Creating public chat of hive
    chat = ChChat()
    chat.set_hive(hive=hive)
    chat.save()
    chat.join(profile)

    # Creating subscription
    subscription = ChSubscription()
    subscription.set_hive(hive=hive)
    subscription.set_profile(profile=profile)
    subscription.set_chat(chat=chat)
    subscription.save()

    return HttpResponseRedirect("/home/")


@login_required
def join(request, hive_name):
    """
    :param request:
    :param hive_name: Name of the hive that will be joined to
    :return: Home web page with the subscription created
    """
    # Getting needed information
    username = request.user
    user = ChUser.objects.get(username=username)
    profile = ChProfile.objects.get(user=user)
    hive_joining = ChHive.objects.get(name=hive_name)

    # Trying to get all the subscriptions of this profile and all the hives he's subscribed to
    try:
        subscriptions = ChSubscription.objects.all()
        subscriptions = subscriptions.filter(profile=profile)
        hives = []
        for subscription in subscriptions:
            # Excluding duplicated hives
            hive_appeared = False
            for hive in hives:
                if subscription.hive == hive:
                    hive_appeared = True
            if not hive_appeared:
                # Adding the hive to the hives array (only hives subscribed)
                hives.append(subscription.hive)
    except ChSubscription.DoesNotExist:
        return HttpResponse("You've no subscriptions yet!")

    # print(hives)
    # print("====================")
    # print(hive_joining)
    hive_appeared = False
    for hive_aux in hives:
        if hive_aux == hive_joining:
            hive_appeared = True

    if not hive_appeared:
        # Getting public chat of hive
        chat = ChChat.objects.get(hive=hive_joining)

        # Creating subscription
        subscription = ChSubscription()
        subscription.set_hive(hive=hive_joining)
        subscription.set_profile(profile=profile)
        subscription.set_chat(chat=chat)
        subscription.save()

    else:
        return HttpResponse("You're already subscribed to this hive")

    return HttpResponseRedirect("/home/")


@login_required
def home(request):
    """
    :param request:
    :return: Home web page
    """
    if request.method == 'GET':
        # Getting needed info
        username = request.user
        user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=user)

        # Trying to get all the subscriptions of this profile
        try:
            subscriptions = ChSubscription.objects.all()
            subscriptions = subscriptions.filter(profile=profile)
            hives = []
            for subscription in subscriptions:
                # Excluding duplicated hives
                hive_appeared = False
                for hive in hives:
                    if subscription.hive == hive:
                        hive_appeared = True
                if not hive_appeared:
                    # Adding the hive to the home view
                    hives.append(subscription.hive)
        except ChSubscription.DoesNotExist:
            subscriptions, subscription = None
        # print(subscriptions)
        return render(request, "core/home.html", {
            'hives': hives
        })


@login_required
def explore(request):
    """
    :param request:
    :return: Explore web page which contains all hives
    """
    if request.method == 'GET':
        # Returns all the hives (subscribed and not subscribed)
        try:
            hives = ChHive.objects.all()
        except ChHive.DoesNotExist:
            hives = None
        return render(request, "core/explore.html", {
            'hives': hives
        })


@login_required
def profile(request, private):
    """
    :param request:
    :param private: Type of profile which is going to be shown, private or public
    :return: Profile web page which contains your personal info
    """
    if request.method == 'GET':
        username = request.user
        try:
            user = ChUser.objects.get(username=username)
            profile = ChProfile.objects.get(user=user)
        except ChProfile.DoesNotExist, ChUser.DoesNotExist:
            profile, user = None
        if private == "private":
            data = {"first_name": profile.first_name, "surname": profile.last_name, "language": profile.language,
                    "sex": profile.sex}
            return render(request, "core/private_profile.html", {
                "profile": data
            })
        elif private == "public":
            data = {"public_name": profile.public_name, "language": profile.language,
                    "location": profile.location, "show_age": profile.public_show_age}
            return render(request, "core/public_profile.html", {
                "profile": data
            })
        else:
            return HttpResponse("Error")


@login_required
def chat(request, hive):
    """
    :param request:
    :param hive: Name of the hive, which will be used for the channel name in Pusher
    :return: Chat web page which allows to chat with users who joined the same channel
    """
    # Variable declaration
    user = request.user.get_username()
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'
    hive = hive.replace(" ", "_")
    hive2 = replace_unicode(hive)
    channel = hive2
    print(channel)  # PRINT

    # GET vs POST
    if request.method == 'POST':

        msg = request.POST.get("message")
        timestamp = request.POST.get("timestamp")
        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret
        )
        print(channel + " aqui se envia")  # PRINT
        p[channel].trigger(event, {"username": user, "message": msg, "timestamp": timestamp})
        # request.session.set_expiry(300)
        return HttpResponse("Server Ok")
    else:

        if channel != 'public_test':
            channel = hive2 + '_public'
        print(channel)  # PRINT
        form = MsgForm()
        return render(request, "core/chat_hive.html", {
            'user': user,
            'app_key': app_key,
            'key': key,
            'hive': hive,
            'channel': channel,
            'event': event,
            'form': form,
        })