__author__ = 'lorenzo'
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from chat_app.models import *

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
    channel='public_test'
    event='msg'
    return render(request, "chat_app/chat.html", {
        'user': user,
        'app_key': app_key,
        'key': key,
        'channel' : channel,
        'event' : event
    })