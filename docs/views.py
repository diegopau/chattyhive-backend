# -*- encoding: utf-8 -*-
__author__ = 'xurxo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from core.pusher_extensions import ChPusher


@csrf_exempt
def project_summary(request):
    if request.method == 'GET':
        return render(request, 'docs/project_summary.html')


@csrf_exempt
def api_methods(request):
    if request.method == 'GET':
        return render(request, 'docs/api_methods.html')
