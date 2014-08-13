from django.utils import timezone

__author__ = 'xulegaspi'

import django
import json
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from core.models import ChUser, ChProfile, ChUserManager, ChSubscription, ChHive, ChChat, ChMessage
from django.core.serializers.json import DjangoJSONEncoder
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

            aux = request.body
            data = json.loads(aux.decode('utf-8'))
            data_message = data["MESSAGE"]
            id_data = data["ID"]
            profile_data = data["PROFILE"]
            server_timestamp_data = data["SERVER_TIMESTAMP"]
            channel_unicode_data = data["CHANNEL_UNICODE"]
            confirmed_data = data["CONFIRMED"]
            content_data = data["CONTENT"]
            timestamp_data = data["TIMESTAMP"]

            msg = content_data['CONTENT']
            msg_type = content_data['CONTENT_TYPE']

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
# 0.2 Version            #
# ================================== #
def start_session(request):
    if request.method == 'GET':
        csrf = django.middleware.csrf.get_token(request)
        csrf_answer = {'CSRF': csrf}
        return HttpResponse(json.dumps({'CSRF_TOKEN': csrf_answer}),
                            mimetype="application/json")
    else:
        raise Http404


def login_v2(request):
    if request.method == 'POST':
        aux = request.body
        data = json.loads(aux.decode('utf-8'))
        data_login = data["LOGIN"]
        login_string = data_login['USER']
        passw = data_login['PASS']
        status = "OK"
        error = None
        logs = {"user": login_string, "pass": passw}
        print(logs)  # PRINT

        if '@' in login_string:
            user = ChUser.objects.get(email=login_string)
            user = authenticate(username=user.username, password=passw)
            profile = ChProfile.objects.get(user=user)
        else:
            profile = ChProfile.objects.select_related().get(public_name=login_string)
            user = authenticate(username=profile.username, password=passw)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = profile.username
                request.session['active'] = True
                # request.user = user
                session_id = request.session.session_key
                logs = {"user": login_string, "pass": passw, "session": session_id}
                status = "OK"
                common = {"STATUS": status, "ERROR": error}
                answer = json.dumps({"COMMON": common, "LOGS": logs}, cls=DjangoJSONEncoder)
                # return HttpResponse(answer, mimetype="application/json")
                return HttpResponse(answer)
                # return HttpResponseRedirect("/home/")
            else:
                status = 'ERROR'
                error = 'User is not active'
                common = {"STATUS": status, "ERROR": error}
                answer = json.dumps({"COMMON": common, "LOGS": logs}, cls=DjangoJSONEncoder)
                return HttpResponse(answer, mimetype="application/json")
        else:
            status = 'ERROR'
            error = 'User auth is None'
            common = {"STATUS": status, "ERROR": error}
            answer = json.dumps({"COMMON": common, "LOGS": logs}, cls=DjangoJSONEncoder)
            return HttpResponse(answer, mimetype="application/json")
    else:
        status = "ERROR"
        error = 'Invalid method'
        common = {"STATUS": status, "ERROR": error}
        answer = json.dumps({"COMMON": common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")
        # raise Http404


def explore(request):
    if request.method == 'GET':
        status = 'OK'
        error = None
        # Returns all the hives (subscribed and not subscribed)
        hive_array = []
        try:
            hives = ChHive.objects.all()
            for hive in hives:
                hive_array.append({'HIVE': hive.toJSON()})
            status = 'OK'
        except ChHive.DoesNotExist:
            status = 'OK'
        hive_answer = {'LIST': hive_array}
        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common, 'HIVE_LIST': hive_answer}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")
    else:
        status = 'ERROR'
        error = 'Invalid method'
        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def email_check(request, user_email):
    """
    :param request:
    :return: JSON with status
    """

    if request.method == 'GET':

        # Getting email from POST param
        status = "OK"
        error = None

        # Checking already existing user
        try:
            if ChUser.objects.get(email=user_email) is not None:
                status = "ERROR"
                error = "User already exists"
        except ObjectDoesNotExist:
            status = "OK"

        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")

    else:
        status = "ERROR"
        error = "Invalid method"
        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def register(request):
    """
    :param request:
    :return: JSON with status and profile
    """

    if request.method == 'POST':

        # Getting all parameters from POST
        aux = request.body
        data = json.loads(aux.decode('utf-8'))

        local_user_profile_data = data['LOCAL_USER_PROFILE']
        login_data = data['LOGIN']
        public_data = local_user_profile_data['USER_PUBLIC_PROFILE']
        private_data = local_user_profile_data['USER_PRIVATE_PROFILE']

        email = local_user_profile_data['EMAIL']
        password = login_data['PASS']
        public_name = public_data['PUBLIC_NAME']
        location = public_data['LOCATION']
        sex = public_data['SEX']
        birthdate = public_data['BIRTHDATE']
        language = public_data['LANGUAGE']
        public_show_age = public_data['PUBLIC_SHOW_AGE']
        public_show_sex = public_data['PUBLIC_SHOW_SEX']
        public_show_location = public_data['PUBLIC_SHOW_LOCATION']
        user_color = public_data['USER_COLOR']
        image_url = public_data['IMAGE_URL']
        user_id = private_data['USER_ID']
        first_name = private_data['FIRST_NAME']
        last_name = private_data['LAST_NAME']
        private_show_age = private_data['PRIVATE_SHOW_AGE']

        status = "OK"
        error = None

        username = email
        # password = pass1
        # print(username + '_ANDROID')  # PRINT

        try:
            # Checking already existing user
            if ChUser.objects.get(username=username) is not None:
                status = "ERROR"
                error = "User already exists"
                common = {'STATUS': status, 'ERROR': error}
                answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
                return HttpResponse(answer, mimetype="application/json")

        except ObjectDoesNotExist:

            # Creating the new user
            manager = ChUserManager()
            user = manager.create_user(username, email, password)

            # Creating the profile
            profile = ChProfile(user=user)
            profile.save()

            # Inserting info to the profile
            profile.public_name = public_name
            profile.first_name = first_name
            profile.last_name = last_name
            profile.sex = sex
            profile.birth_date = birthdate
            profile.language = language
            # profile.location = location
            profile.set_approximate_location(location)
            profile.personal_color = user_color
            profile.private_show_age = private_show_age
            profile.public_show_age = public_show_age
            profile.public_show_location = public_show_location
            profile.public_show_sex = public_show_sex
            profile.save()

            # Formatting info for sending in json
            # profile_json = json.dumps({"set_public_name": public_name,
            #                            "set_first_name": first_name,
            #                            "set_last_name": last_name,
            #                            "set_sex": sex,
            #                            "set_language": language,
            #                            "set_private_show_age": private_show_age,
            #                            "set_public_show_age": public_show_age,
            #                            "set_show_location": public_show_location,
            #                            "set_location": location})

            # Sending info to Android device
            status = "OK"
            error = None
            common = {'STATUS': status, 'ERROR': error}
            answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
            return HttpResponse(answer, mimetype="application/json")
            # return HttpResponse(json.dumps({
            #     'status': status,  # Returning OK status
            #     'profile': profile_json  # Returning complete Profile
            # }))

    else:
        status = "ERROR"
        error = "Invalid method"
        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def join(request):
    if request.method == 'POST':
        # Getting params from POST
        aux = request.body
        data = json.loads(aux.decode('utf-8'))
        hive_name = data['hive']
        username = data['user']

        # Processing params to get info in server
        user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=user)
        hive_joining = ChHive.objects.get(name=hive_name)

        # Trying to get all the subscriptions of this profile and all the hives he's subscribed to
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
                    # Adding the hive to the hives array (only hives subscribed)
                    hives.append(subscription.hive.toJSON())
        except ChSubscription.DoesNotExist:
            return HttpResponse("Subscription not found")

        # Checking if the user is already subscribed to this hive
        hive_appeared = False
        for hive_aux in hives:
            if hive_aux == hive_joining:
                hive_appeared = True

        # Joining to this hive
        if not hive_appeared:
            # Getting public chat of hive
            chat2 = ChChat.objects.get(hive=hive_joining)

            # Creating subscription
            subscription = ChSubscription()
            subscription.hive = hive_joining
            subscription.profile = profile
            subscription.chat = chat2
            subscription.save()

            status = 'SUBSCRIBED'
            return HttpResponse(json.dumps({'status': status}, cls=DjangoJSONEncoder), mimetype="application/json")

        else:
            status = 'ALREADY_SUBSCRIBED'
            return HttpResponse(json.dumps({'status': status}, cls=DjangoJSONEncoder), mimetype="application/json")
    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}), mimetype="application/json")
        # raise Http404


def chat_v2(request):
    # Variable declaration
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'

    # GET vs POST
    if request.method == 'POST':
        # Getting params from POST
        aux = request.body
        data = json.loads(aux.decode('utf-8'))
        hive_name = data['hive']
        username = data['user']
        msg = data['message']
        timestamp = data['timestamp']

        # Processing params to get info in server
        user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=user)
        hive = ChHive.objects.get(name=hive_name)
        # hive_url = hive.name_url

        chat2 = ChChat.objects.get(hive=hive)

        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret,
            encoder=DjangoJSONEncoder,
        )
        message = ChMessage(profile=profile, chat=chat2)
        message.date = timezone.now()
        message.content_type = 'text'
        message.content = msg

        p[chat2.channel_unicode].trigger(event, {"username": user.username,
                                                 "public_name": profile.public_name,
                                                 "message": msg,
                                                 "timestamp": timestamp,
                                                 "server_time": message.date.astimezone(),
        })

        message.save()

        status = 'MESSAGE_SENT'
        return HttpResponse(json.dumps({'status': status}, cls=DjangoJSONEncoder), mimetype="application/json")
    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}), mimetype="application/json")
        # raise Http404


def recover_local_user_profile(request):
    if request.method == 'GET':
        usern = request.session['user']
        user = ChUser.objects.get(username=usern)
        profile = ChProfile.objects.get(user=user)
        email = user.email
        status = "OK"
        error = None

        public_profile = json.loads(profile.toJSON(True))

        private_profile = json.loads(profile.toJSON(False))

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
                    if subscription.hive:
                        hives.append({"HIVE_ID": {"NAME_URL": subscription.hive.name_url}})
        except ChSubscription.DoesNotExist:
            status = "ERROR"
            error = "Subscription not found"
            hives = None

        common = {'STATUS': status, 'ERROR': error}
        local_user_profile = {'EMAIL': email, 'HIVES_SUBSCRIBED': hives, 'USER_PUBLIC_PROFILE': public_profile,
                              'USER_PRIVATE_PROFILE': private_profile}
        answer = json.dumps({'COMMON': common, 'LOCAL_USER_PROFILE': local_user_profile}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def get_chat_context(request, chat_id):
    if request.method == 'GET':
        usern = request.session['user']
        user = ChUser.objects.get(username=usern)
        # profile = ChProfile.objects.get(user=user)
        chat = ChChat.objects.get(channel_unicode=chat_id)
        status = "OK"
        error = None
        pusher_channel = chat.channel(chat_id)
        creation_date = None
        parent_hive = None
        try:
            members = []
            subscriptions = ChSubscription.objects.filter(chat=chat)
            for subscription in subscriptions:
                user_id = None
                public_name = subscription.profile.public_name
                profile_id = {'USER_ID': user_id, 'PUBLIC_NAME': public_name}
                members.append(profile_id)
        except ChSubscription.DoesNotExist:
            members = None

        common = {'STATUS': status, 'ERROR': error}
        chat_answer = {'CHANNEL_UNICODE': chat_id, 'PUSHER_CHANNEL': pusher_channel, 'MEMBERS': members,
                       'CREATION_DATE': creation_date, 'PARENT_HIVE': parent_hive}
        answer = json.dumps({'COMMON': common, 'CHAT': chat_answer}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def get_chat_list(request):
    if request.method == 'GET':
        usern = request.session['user']
        try:
            user = ChUser.objects.get(username=usern)
            # user = request.user
            profile = ChProfile.objects.get(user=user)
            print(user)
            status = "OK"
            error = None
            try:
                subscriptions = ChSubscription.objects.filter(profile=profile)
                chats_sync = []
                for subscription in subscriptions:
                    message = ChMessage.objects.filter(chat=subscription.chat).order_by('-id')[0]
                    id = message.id
                    profile1 = message.profile.public_name
                    server_timestamp = None
                    channel_unicode = subscription.chat.channel_unicode
                    confirmed = False
                    content_type = message.content_type
                    content = message.content
                    content = {'CONTENT_TYPE': content_type, 'CONTENT': content}
                    timestamp = None
                    message_answer = {'ID': id, 'PROFILE': profile1, 'SERVER_TIMESTAMP': server_timestamp,
                                      'CHANNEL_UNICODE': channel_unicode, 'CONFIRMED': confirmed,
                                      'CONTENT': content, 'TIMESTAMP': timestamp}
                    chat_sync = {'CHANNEL_UNICODE': channel_unicode, 'LAST_MESSAGE': message_answer}
                    chat_sync = {'CHAT_SYNC': chat_sync}
                    chats_sync.append(chat_sync)
            except ChSubscription.DoesNotExist:
                status = "ERROR"
                error = "Does not exist"
        except (ChUser.DoesNotExist, ChProfile.DoesNotExist):
            status = "ERROR"
            error = "User/Profile does not exist"

        common = {'STATUS': status, 'ERROR': error}
        list_aux = {'LIST': chats_sync}
        answer = json.dumps({'COMMON': common, 'CHAT_LIST': list_aux}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")


def create_hive(request):
    if request.method == 'POST':
        status = "OK"
        error = None
        usern = request.session['user']

        try:
            aux = request.body
            data = json.loads(aux)

        except(Exception):
            status = "ERROR"
            error = None


def get_hive_info(request, hive_id):
    if request.method == 'GET':
        status = "OK"
        error = None

        hive = ChHive.objects.get(name_url=hive_id)

        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common, 'HIVE': hive.toJSON()}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")
    else:
        status = 'ERROR'
        error = 'Invalid method'
        common = {'STATUS': status, 'ERROR': error}
        answer = json.dumps({'COMMON': common}, cls=DjangoJSONEncoder)
        return HttpResponse(answer, mimetype="application/json")



