__author__ = 'lorenzo'
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from chat_app.models import *

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        return HttpResponseRedirect("/chat/")
    else:
        form = LoginForm()
    #return HttpResponse("Hello, world. You're at the poll index.")
    return render(request, "chat_app/login.html", {
        'form':form
    })

def chat(request):
    return render_to_response('chat_app/chat.html')