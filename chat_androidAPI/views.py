import django
import json
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from core.models import ChUser, ChProfile, ChUserManager, ChSubscription

__author__ = 'lorenzo'

from django.http import HttpResponse, Http404
import pusher


# @csrf_exempt
def login(request, user):
    """
    :param request:
    :param user: username for the login request
    :return: JSON with status, csrf and session_id
    """
    if request.method == 'GET':
        # print("if")  # PRINT
        request.session['user'] = user
        request.session['active'] = True
        request.session.set_expiry(300)
        session_id = request.session.session_key
        csrf = django.middleware.csrf.get_token(request)
        status = "LOGGED"
        # print(status)  # PRINT
        return HttpResponse(json.dumps({'status': status, 'csrf': csrf, 'session_id': session_id}),
                            mimetype="application/json")
    else:
        status = "ERROR"
        # print(status)  # PRINT
        return HttpResponse(json.dumps({"status": status}), mimetype="application/json")


# @csrf_exempt
def chat(request):
    """
    :param request:
    :return: JSON with status
    """
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
def start_session(request):
    if request.method == 'GET':
        csrf = django.middleware.csrf.get_token(request)
        # print(status)  # PRINT
        return HttpResponse(json.dumps({'csrf': csrf}),
                            mimetype="application/json")
    else:
        raise Http404


def login_v2(request):
    if request.method == 'POST':
        user = request.POST.get("user")
        passw = request.POST.get("pass")
        user_auth = authenticate(username=user, password=passw)
        if user_auth is not None:
                if user_auth.is_active:
                    login(request, user)
                    status = "OK"

                    chuser = ChUser.objects.get(username=user)

                    profile = ChProfile.objects.get(user=chuser)

                    # Trying to get all the subscriptions of this profile
                    try:
                        subscriptions = ChSubscription.objects.filter(profile=profile)
                        hives = []
                        for subscription in subscriptions:
                            # Excluding duplicated hives
                            hive_appeared = False
                            for hive in hives:
                                if subscription.hive == hive:
                                    hive_appeared = True
                            if not hive_appeared:
                                # Adding the hive to the home view
                                hives.append(subscription.hive)
                    except ChSubscription.DoesNotExist:
                        return HttpResponse("Subscription not found")

                    answer = json.dumps({'status': status, 'profile': profile, 'hives_subscribed': hives})

                    return HttpResponse(answer)
                    # return HttpResponseRedirect("/home/")
                else:
                    status = 'ERROR'
                    return HttpResponse(json.dumps({'status': status}))
        else:
            status = 'ERROR'
            return HttpResponse(json.dumps({'status': status}))
    else:
        raise Http404


def explore(request):
    if request.method == 'GET':
        # Returns all the hives (subscribed and not subscribed)
        try:
            hives = ChHive.objects.all()
            status = "OK"
        except ChHive.DoesNotExist:
            hives = None
            status = "NO HIVES"

        answer = json.dumps({'status': status, 'hives': hives})
        return HttpResponse(answer)


def email_check(request):
    """
    :param request:
    :return: JSON with status
    """

    if request.method == 'POST':

        # Getting email from POST param
        email = request.POST.get('email')

        username = email
        # print(email + '_ANDROID')  # PRINT

        # Checking already existing user
        try:
            if ChUser.objects.get(username=username) is not None:
                status = "USER_ALREADY_EXISTS"
        except ObjectDoesNotExist:
            status = "OK"

        return HttpResponse(json.dumps({'status': status}))

    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}))


def register(request):
    """
    :param request:
    :return: JSON with status and profile
    """

    if request.method == 'POST':

        # Getting all parameters from POST
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        public_name = request.POST.get('public_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        sex = request.POST.get('sex')
        language = request.POST.get('language')
        private_show_age = request.POST.get('private_show_age')
        location = request.POST.get('location')
        public_show_age = request.POST.get('public_show_age')
        show_location = request.POST.get('show_location')

        username = email
        password = pass1
        # print(username + '_ANDROID')  # PRINT

        try:
            # Checking already existing user
            if ChUser.objects.get(username=username) is not None:
                status = "USER_ALREADY_EXISTS"
                return HttpResponse(json.dumps({"status": status}))

        except ObjectDoesNotExist:

            # Creating the new user
            manager = ChUserManager()
            user = manager.create_user(username, email, password)

            # Creating the profile
            profile = ChProfile(user=user)
            profile.save()

            # Inserting info to the profile
            profile.set_public_name(public_name)
            profile.set_first_name(first_name)
            profile.set_last_name(last_name)
            profile.set_sex(sex)
            profile.set_language(language)
            profile.set_private_show_age(private_show_age)
            profile.set_public_show_age(public_show_age)
            profile.set_show_location(show_location)
            profile.set_location(location)
            profile.save()

            # Formatting info for sending in json
            profile_json = json.dumps({"set_public_name": public_name,
                                       "set_first_name": first_name,
                                       "set_last_name": last_name,
                                       "set_sex": sex,
                                       "set_language": language,
                                       "set_private_show_age": private_show_age,
                                       "set_public_show_age": public_show_age,
                                       "set_show_location": show_location,
                                       "set_location": location})

            # Sending info to Android device
            status = "PROFILE_CREATED"
            return HttpResponse(json.dumps({
                'status': status,   # Returning OK status
                'profile': profile_json  # Returning complete Profile
            }))

    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}))


