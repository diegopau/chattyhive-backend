import django, json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from core.models import ChUser, ChProfile, ChUserManager

__author__ = 'lorenzo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import pusher


# @csrf_exempt
def login(request, user):
    if request.method == 'GET':
        print("if")
        request.session['user'] = user
        request.session['active'] = True
        request.session.set_expiry(300)
        session_id = request.session.session_key
        csrf = django.middleware.csrf.get_token(request)
        status = "LOGGED"
        print(status)
        return HttpResponse(json.dumps({'status': status, 'csrf': csrf, 'session_id': session_id}),
                            mimetype="application/json")
    else:
        status = "ERROR"
        print(status)
        return HttpResponse(json.dumps({"status": status}), mimetype="application/json")


# @csrf_exempt
def chat(request):
    # Variable declaration
    if 'user' in request.session and request.session['active']:
        user = request.session['user']
        app_key = "55129"
        key = 'f073ebb6f5d1b918e59e'
        secret = '360b346d88ee47d4c230'
        channel = 'public_test'
        event = 'msg'

        # GET vs POST
        if request.method == 'POST':

            msg = request.POST.get("message")
            timestamp = request.POST.get("timestamp")
            p = pusher.Pusher(
                app_id=app_key,
                key=key,
                secret=secret
            )
            p[channel].trigger(event, {"username": user, "message": msg, "timestamp": timestamp})
            request.session.set_expiry(300)
            status = "RECEIVED"
            return HttpResponse({"status": status})
        else:
            status = "ERROR"
            return HttpResponse({"status": status})
    else:
        status = "EXPIRED"
        return HttpResponse({"status": status})


# ================================== #
#             0.2 Version            #
# ================================== #
def create_user_view(request, email, pass1, pass2):
    if request.method == 'POST':
        # username = form.cleaned_data['username']
        email = email
        username = email  # TODO temporal solution, should be changed
        password = pass1
        password2 = pass2
        print(email)
        print(password)

        if password == password2:  # Checking correct password written twice
            # Checking already existing user
            try:
                if ChUser.objects.get(username=username) is not None:
                    status = "ALREADY_EXISTS"
                    return HttpResponse({"status": status})
            except ObjectDoesNotExist:
                manager = ChUserManager()
                user = manager.create_user(username, email, password)
        else:
            status = "NOT_MATCHING_PASS"
            return HttpResponse({"status": status})

        # Let's try to create a linked profile here
        profile = ChProfile(user=user)
        profile.save()

        # Let's try to save the user in a cookie
        request.session['email'] = profile.user.username
        request.session['pass'] = password

        return HttpResponseRedirect("/create_user/register1/")

    else:
        # print(form.errors)
        return HttpResponse("ERROR, invalid form")