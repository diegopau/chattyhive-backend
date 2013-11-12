import datetime

__author__ = 'lorenzo'
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from chat_app.models import *
from django.contrib import auth
import pusher


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.cleaned_data['user']
            # request.session['active'] = True
            request.session.set_expiry(300)
            # print(request.session.get_expiry_age())
            return HttpResponseRedirect("/chat/")
    else:
        if 'user' in request.session:
        # if 'active' in request.session and request.session['active']:
            # request.session['active'] = False
            print('one')
            # print(request.session.get_expiry_age())
            request.session.set_expiry(300)
            return HttpResponseRedirect("/chat/")
        form = LoginForm()
        print('two')
        return render(request, "chat_app/login.html", {
            'form': form
        })


def chat(request):
    # Variable declaration
    user = request.session['user']
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    channel = 'public_test'
    event = 'msg'

    # GET vs POST
    if request.method == 'POST':
        # print("post")
        # if request.is_ajax():
        #     print("ajax")

        msg = request.POST.get("msg")
        # loc_user = request.get('user')
        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret
        )
        # print(loc_user)
        # print(msg)
        p[channel].trigger(event, {"user": user, "msg": msg})
        request.session.set_expiry(300)
        return HttpResponse("=>sended")
        # return HttpResponse("nope")

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