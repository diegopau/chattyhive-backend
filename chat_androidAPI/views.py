__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import pusher

def login(request):
    if request.method == 'POST':
        print("if")
        # form = LoginForm(request.POST)
        # if form.is_valid():
        #     status="LOGGED"
        #     return HttpResponse({"status": status})
        # else:
        #     status="ERROR"
        #     return HttpResponse({"status": status})

    else:
        status="ERROR"
        return HttpResponse({"status": status})

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

            msg = request.POST.get("msg")
            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret
            )
            p[channel].trigger(event, {"user": user, "msg": msg})
            request.session.set_expiry(300)
            status="RECEIVED"
            return HttpResponse({"status": status})
        else:
            status="ERROR"
            return HttpResponse({"status": status})
    else:
        status="NOLOGGED"
        return HttpResponse({"status": status})