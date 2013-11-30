from django.views.decorators.csrf import csrf_exempt

__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import pusher

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print("if")
        request.session['user'] = request.POST.get["username"]
        request.session['active'] = True
        request.session.set_expiry(300)
        session_id=request.session.session_key
        status="LOGGED"
        return HttpResponse({"status": status, "session": session_id})
    else:
        status="ERROR"
        return HttpResponse({"status": status})

@csrf_exempt
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
            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret
            )
            p[channel].trigger(event, {"username": user, "message": msg, "timestamp": timestamp})
            request.session.set_expiry(300)
            status="RECEIVED"
            return HttpResponse({"status": status})
        else:
            status="ERROR"
            return HttpResponse({"status": status})
    else:
        status="EXPIRED"
        return HttpResponse({"status": status})