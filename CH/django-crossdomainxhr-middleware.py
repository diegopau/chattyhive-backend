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

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            print("ACCESS_CONTROL_REQUEST_METHOD - AngularJS")
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
            if request.method == 'OPTIONS':
                # response = http.HttpResponse()
                # request['Origin']

                print("OPTION METHOD - AngularJS - Browser")
                response['Access-Control-Allow-Origin'] = request.META['HTTP_Origin']
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = ['POST', 'GET', 'OPTIONS']
                response['Access-Control-Allow-Headers'] = '*'
                response['Content-type'] = ['text/html', 'charset=utf-8']

            return response

        if request.method == 'OPTIONS':
            response = http.HttpResponse()
            # request['Origin']

            print("OPTION METHOD - AngularJS - Browser")
            response['Access-Control-Allow-Origin'] = request.META['Origin']
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = ['POST', 'GET', 'OPTIONS']
            response['Access-Control-Allow-Headers'] = '*'
            response['Content-type'] = ['text/html', 'charset=utf-8']

            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response

    def options_response(self, request):
        print("EN EL METODO ENTRA...")

#             Access-Control-Allow-Origin: http://api.bob.com
# Access-Control-Allow-Methods: GET, POST, PUT
# Access-Control-Allow-Headers: X-Custom-Header
# Content-Type: text/html; charset=utf-8