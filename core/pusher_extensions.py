# -*- encoding: utf-8 -*-

__author__ = 'lorenzo'

import hashlib
import hmac
from django.core.serializers import json
from pusher import Pusher


class ChPusher(Pusher):

    def webhook(self, request):
        return WebHook(self, request)


class WebHook(object):

    def __init__(self, pusher, request):
        self.pusher = pusher
        self.request_body = request.body
        self.data = json.loads(request.body)
        self.header_key = request.META.get('HTTP_X_PUSHER_KEY')
        self.header_signature = request.META.get('HTTP_X_PUSHER_SIGNATURE')

    def is_valid(self):
        if self.header_key != self.pusher.key:
            return False
        signature = hmac.new(self.pusher.secret, self.request_body, hashlib.sha256).hexdigest()
        return self.header_signature == signature

    def events(self):
        return self.data['events']

    def time(self):
        return self.data['time_ms']