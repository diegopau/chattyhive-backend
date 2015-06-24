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
def pusher_webhooks(request):
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'

    # GET vs POST
    if request.method == 'POST':
        p = ChPusher(
            app_id=app_key,
            key=key,
            secret=secret,
            encoder=DjangoJSONEncoder,
        )

        webhook = p.webhook(request)
        if webhook.is_valid():
            for event in webhook.events():
                print(event)
                if event == 'member_added':
                    if event['channel'] == 'presence' + event['user_id']:
                        print('self')

        else:
            raise Http404
    else:
        raise Http404