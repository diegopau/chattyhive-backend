__author__ = 'lorenzo'
from django.shortcuts import render
from django.http import HttpResponseRedirect
from chat_app.models import *
import pusher

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user']=form.cleaned_data['user']
            return HttpResponseRedirect("/chat/")
    else:
        form = LoginForm()
    return render(request, "chat_app/login.html", {
        'form':form
    })

def chat(request):
    user=request.session['user']
    app_key="55129"
    key='f073ebb6f5d1b918e59e'
    secret ='360b346d88ee47d4c230'
    channel='public_test'
    event='msg'
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            msg=form.cleaned_data['value']
            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret
            )
            p[channel].trigger(event, {"user":user,"msg":msg})

    else:
        return render(request, "chat_app/chat.html", {
            'user': user,
            'app_key': app_key,
            'key': key,
            'channel' : channel,
            'event' : event
        })
