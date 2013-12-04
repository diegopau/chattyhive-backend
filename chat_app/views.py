import datetime

__author__ = 'lorenzo'
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from chat_app.models import *
import os
import pusher


def login(request):
    if request.method == 'POST':
        print("if")
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.cleaned_data['user']
            request.session['active'] = True
            request.session.set_expiry(300)
            return HttpResponseRedirect("/chat/")
        else:
            HttpResponse("ERROR, invalid form")
    else:
        # print("21 /b",request.session['active'])
        if 'user' in request.session and request.session['active'] == True:
            print('one')
            request.session.set_expiry(300)
            return HttpResponseRedirect("/chat/")
        else:
            form = LoginForm()
            print('two')
            return render(request, "chat_app/login.html", {
                'form': form
            })


def chat(request):
    # Variable declaration
    if 'user' in request.session and request.session['active']:
        user = request.session['user']
        app_key = "55129"
        key = 'f073ebb6f5d1b918e59e'
        secret = '360b346d88ee47d4c230'
        channel = 'public_test'
        event = 'msg'

        # GET vs POST
        if request.method == 'POST':

            msg = request.POST.get("message")
            timestamp = request.POST.get("timestamp")
            # os.environ['TZ']
            # tz = datetime.time.tzinfo
            # timestamp_server = datetime.datetime.now().strftime("%xT%X%Z")
            timestamp_server = datetime.datetime.utcnow().isoformat()
            print timestamp_server
            print os.environ['TZ']
            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret
            )
            p[channel].trigger(event, {"username": user, "message": msg, "timestamp": timestamp,
                                       "timestamp_server": timestamp_server})
            request.session.set_expiry(300)
            return HttpResponse("Server Ok")
        else:

            form = MsgForm()
            return render(request, "chat_app/chat.html", {
                'user': user,
                'app_key': app_key,
                'key': key,
                'channel': channel,
                'event': event,
                'form': form,
            })
    else:
        # return HttpResponseRedirect("/")
        return HttpResponse("Session Expired")


def logout(request):
    print("logout")
    # print("11 /b",request.session['active'])
    request.session['active'] = False
    # print("12 /b",request.session['active'])
    return HttpResponse("logged out")