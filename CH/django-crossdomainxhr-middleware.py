__author__ = 'Xurxo'

import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

try:
    import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.


        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if request.method == 'OPTIONS':
            print("OPTION METHOD - AngularJS - Browser")
            string = 'POST, GET, PUT'
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = string
            response['Access-Control-Allow-Headers'] = request.META['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']
            response['Content-type'] = ['text/html', 'charset=utf-8']

            return response

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            print("ACCESS_CONTROL_REQUEST_METHOD - AngularJS")
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

            if request.method == 'OPTIONS':
                print("OPTION METHOD - AngularJS - Browser")
                response['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = ['POST', 'GET', 'OPTIONS']
                response['Access-Control-Allow-Headers'] = request.META['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']
                response['Content-type'] = ['text/html', 'charset=utf-8']

            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            print("RESPONSE-HAS-ACCESS-CONTROL-ALLOW-ORIGIN")
            return response

        print("RESPONSE-1")
        # response['Access-Control-Allow-Credentials'] = 'true'

        # if request.method == 'POST':
        allowed = request.META['HTTP_ORIGIN']
        response['Access-Control-Allow-Credentials'] = 'true'
        # else:
        # allowed = XS_SHARING_ALLOWED_ORIGINS

        # try:
        #     allowed = request.META['HTTP_ORIGIN']
        # except (Exception):

        response['Access-Control-Allow-Origin'] = allowed
        # response['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)

        return response