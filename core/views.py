__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from django.contrib.auth.decorators import login_required


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
    username = request.user
    user = ChUser.objects.get(username=username)
    profile = ChProfile.objects.get(user=user)
    aux = profile.location
    print(aux)
    hive_name = request.session['hive']
    hive = ChHive.objects.get(name=hive_name)

    subscription = ChSubscription()
    subscription.set_hive(hive=hive)
    subscription.set_profile(profile=profile)
    subscription.save()

    return render(request, "core/home.html")


@login_required
def home(request):
    if request.method == 'GET':
        return render(request, "core/home.html")