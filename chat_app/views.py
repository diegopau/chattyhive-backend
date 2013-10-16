__author__ = 'lorenzo'
from django.shortcuts import render
from django.http import HttpResponseRedirect
from chat_app.models import *

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        return HttpResponseRedirect("bienvenido")
    else:
        form = LoginForm()
    #return HttpResponse("Hello, world. You're at the poll index.")
    return render(request, "chat_app/login.html", {
        'form':form
    })
