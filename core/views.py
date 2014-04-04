# -*- encoding: utf-8 -*-
__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from django.contrib.auth.decorators import login_required
import pusher
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone


@login_required
def create_hive(request):
    """
    :param request:
    :return: Web page with the form for creating a hive
    """
    if request.method == 'POST':
        form = CreateHiveForm(request.POST)
        if form.is_valid():
            hive_name = form.cleaned_data['name']
            hive = form.save(commit=False)
            hive.name_url = hive_name.replace(" ", "_")
            hive.save()

            user = request.user
            profile = ChProfile.objects.get(user=user)

            # Creating public chat of hive
            chat = ChChat()
            chat.set_hive(hive=hive)
            chat.set_channel(replace_unicode(hive.name_url))
            chat.save()
            chat.join(profile)

            # Creating subscription
            user = request.user
            profile = ChProfile.objects.get(user=user)
            subscription = ChSubscription()
            subscription.set_hive(hive=hive)
            subscription.set_profile(profile=profile)
            subscription.set_chat(chat=chat)
            subscription.save()
            # return HttpResponseRedirect("/create_hive/create/")
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateHiveForm()
        return render(request, "core/create_hive.html", {
            'form': form
        })


@login_required
def join(request, hive_name):
    """
    :param request:
    :param hive_name: Name of the hive that will be joined to
    :return: Home web page with the subscription created
    """
    if request.method == 'GET':
        # Getting needed information
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive_joining = ChHive.objects.get(name=hive_name)

        # Trying to get all the subscriptions of this profile and all the hives he's subscribed to
        try:
            subscriptions = ChSubscription.objects.filter(profile=profile)
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
            return HttpResponse("Subscription not found")

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
            return HttpResponseRedirect("/home/")

        else:
            return HttpResponse("You're already subscribed to this hive")
    else:
        raise Http404


@login_required
def leave(request, hive_name):
    """
    :param request:
    :param hive_name:
    :return:
    """
    if request.method == 'GET':
        # Getting needed information
        username = request.user
        user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=user)
        hive_leaving = ChHive.objects.get(name=hive_name)

        # Trying to get all the subscriptions of this profile and all the hives he's subscribed to
        try:
            subscriptions = ChSubscription.objects.all()
            subscriptions = subscriptions.filter(profile=profile)
            subscription = subscriptions.filter(hive=hive_leaving)
            subscription.delete()

        except ChSubscription.DoesNotExist:
            return HttpResponse("Subscription not found")

        return HttpResponseRedirect("/home/")
    else:
        raise Http404


@login_required
def home(request):
    """
    :param request:
    :return: Home web page
    """
    if request.method == 'GET':
        # Getting needed info
        user = request.user
        profile = ChProfile.objects.get(user=user)

        # Trying to get all the subscriptions of this profile
        try:
            subscriptions = ChSubscription.objects.filter(profile=profile)
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
            return HttpResponse("Subscription not found")
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
    user = request.user
    if request.method == 'GET':
        try:
            profile = ChProfile.objects.get(user=user)
        except ChProfile.DoesNotExist:
            profile = None
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
def chat(request, chat_url):
    """
    :param request:
    :param chat_url: Url of the chat
    :return: Chat web page which allows to chat with users who joined the same channel
    """
    # Variable declaration
    user = request.user
    profile = ChProfile.objects.get(user=user)
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'

    # GET vs POST
    if request.method == 'POST':
        chat = ChChat.objects.get(channel_unicode=chat_url)

        msg = request.POST.get("message")
        timestamp = request.POST.get("timestamp")
        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret,
            encoder=DjangoJSONEncoder,
        )
        message = ChMessage(profile=profile, chat=chat)
        message.date = timezone.now()
        message.content_type = 'text'
        message.content = msg

        p[chat.channel_unicode].trigger(event, {"username": user.username,
                                                "public_name": profile.public_name,
                                                "message": msg,
                                                "timestamp": timestamp,
                                                "server_time": message.date.astimezone(),
                                                })

        message.save()
        return HttpResponse("Server Ok")
    else:
        chat = ChChat.objects.get(channel_unicode=chat_url)

        form = MsgForm()
        return render(request, "core/chat.html", {
            'user': user.username,
            'app_key': app_key,
            'key': key,
            'url': chat_url,
            'channel': chat.channel_unicode,
            'event': event,
            'form': form,
        })


@login_required
def hive(request, hive_url):
    if request.method == 'GET':
        hive = ChHive.objects.get(name_url=hive_url)
        # chat = ChChat.objects.get(hive=hive)
    else:
        raise Http404


@login_required
def get_messages(request, chat_name, init, interval):
    """
    :param request:
    :param chat_name: Url of the chat, which will be used for the query
    :param init: ID of the first message to return
    :param interval: Number of messages to return
    :return: *interval* messages from *init*
    """
    # Variable declaration
    user = request.user
    profile = ChProfile.objects.get(user=user)
    chat = ChChat.objects.get(channel_unicode=chat_name)
    hive = chat.hive
    try:
        ChSubscription.objects.get(profile=profile, hive=hive)
    except ChSubscription.DoesNotExist:
        return HttpResponse("You are not subscribed to this chat")

    # GET vs POST
    if request.method == 'GET':
        # chat = ChChat.objects.get(hive=hive)
        if init == 'last':
            messages = ChMessage.objects.filter(chat=chat).order_by('-id')[0:int(interval)]
        elif init.isnumeric():
            messages = ChMessage.objects.filter(chat=chat, id__lte=int(init)).order_by('-id')[0:int(interval)]
        else:
            raise Http404
        messages_row = []
        for message in messages:
            messages_row.append({"username": message.profile.user.username,
                                 "public_name": message.profile.public_name,
                                 "message": message.content,
                                 "timestamp": message.date.astimezone(),
                                 "server_time": message.date.astimezone(),
                                 "id": message.id
            })
        return HttpResponse(json.dumps(messages_row, cls=DjangoJSONEncoder))
    else:
        raise Http404


def android_test(request):
    return render(request, "core/android_test.html")


def test(request):
    if request.method == 'POST':
        data = request.POST.items()
        headers = request.POST.get("head")
    if request.method == 'GET':
        data = request.GET.items()
        headers = request.GET.get("head")
    return HttpResponse(headers)