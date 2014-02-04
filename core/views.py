from chat_app.models import MsgForm

__author__ = 'lorenzo'

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from django.contrib.auth.decorators import login_required
import pusher


@login_required
def create_hive(request):
    if request.method == 'POST':
        form = CreateHiveForm(request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
            hive = form.cleaned_data['name']
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
    # Getting needed information
    username = request.user
    user = ChUser.objects.get(username=username)
    profile = ChProfile.objects.get(user=user)
    aux = profile.location
    print(aux)
    hive_name = request.session['hive']
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
def home(request):
    if request.method == 'GET':
        username = request.user
        user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=user)
        try:
            # subscriptions = ChSubscription.objects.get(profile=profile)  # TODO receiving more than 1 object
            subscriptions = ChSubscription.objects.all()
            subscriptions = subscriptions.filter(profile=profile)
            # hives = ChSubscription.hive.objects.all()
            hives = []
            for subscription in subscriptions:
                hives.append(subscription.hive)
                print(hives)
            # hives = subscription.all()
            # subscription.hostdata_set.all()
        except ChSubscription.DoesNotExist:
            subscriptions, subscription = None
        print(subscriptions)
        return render(request, "core/home.html", {
            'hives': hives
        })


@login_required
def explore(request):
    if request.method == 'GET':
        username = request.user
        user = ChUser.objects.get(username=username)
        # profile = ChProfile.objects.get(user=user)
        try:
            # subscription = ChSubscription.objects.get(profile=profile)  # TODO receiving more than 1 object
            subscriptions = ChSubscription.objects.all()
            # hives = ChSubscription.hive.objects.all()
            hives = []
            for subscription in subscriptions:
                hives.append(subscription.hive)
                print(hives)
            # hives = subscription.all()
            # subscription.hostdata_set.all()
        except ChSubscription.DoesNotExist:
            subscriptions, subscription = None
        print(subscriptions)
        return render(request, "core/explore.html", {
            'hives': hives
        })


@login_required
def chat(request, hive):
    # Variable declaration
    # if 'user' in request.session and request.session['active']:
    # user = request.session['user']
    user = request.user.get_username()
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'
    channel = hive
    print(channel)

    # GET vs POST
    if request.method == 'POST':

        msg = request.POST.get("message")
        timestamp = request.POST.get("timestamp")
        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret
        )
        print(channel + " aqui se envia")
        p[channel].trigger(event, {"username": user, "message": msg, "timestamp": timestamp})
        # request.session.set_expiry(300)
        return HttpResponse("Server Ok")
    else:

        channel = hive + '_public'
        print(channel)
        form = MsgForm()
        return render(request, "core/chat_hive.html", {
            'user': user,
            'app_key': app_key,
            'key': key,
            'channel': channel,
            'event': event,
            'form': form,
        })