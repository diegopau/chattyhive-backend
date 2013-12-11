__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from chat_app.models import *
from login.models import *
from django.contrib.auth.decorators import login_required
import pusher


@login_required
def chat(request):
    # Variable declaration
    # if 'user' in request.session and request.session['active']:
    # user = request.session['user']
    user = 'user'
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    channel = 'public_test'
    event = 'msg'

    if not request.user.is_authenticated():
        print("nope")
    else:
        print("yep")

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
        # request.session.set_expiry(300)
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