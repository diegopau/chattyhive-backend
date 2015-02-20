# -*- encoding: utf-8 -*-
__author__ = 'xurxo'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from django.contrib.auth.decorators import login_required
import pusher
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from core.pusher_extensions import ChPusher
from core.models import AndroidDevice


@login_required
def create_hive(request):
    """
    :param request:
    :return: Web page with the form for creating a hive
    """
    if request.method == 'POST':
        formHive = CreateHiveForm(request.POST, prefix='formHive')
        formTags = TagForm(request.POST, prefix='formTags')
        if formHive.is_valid() and formTags.is_valid():
            user = request.user
            profile = ChProfile.objects.get(user=user)

            hive_name = formHive.cleaned_data['name']
            hive = formHive.save(commit=False)
            hive.creator = profile
            hive.name_url = hive_name.replace(" ", "_")
            hive.name_url = replace_unicode(hive.name_url)

            try:
                ChHive.objects.get(name_url=hive.name_url)
                return HttpResponse("This hive already exists")
            except ChHive.DoesNotExist:
                # hive.name_url = replace_unicode(hive_name)
                hive.save()

            # Adding tags
            tagsText = formTags.cleaned_data['tags']
            tagsArray = tagsText.split(" ")
            hive.set_tags(tagsArray)
            hive.save()

            # Creating public chat of hive
            chat = ChChat()
            chat.hive = hive
            chat.type = 'public'
            chat.channel = hive.name_url
            chat.save()

            # Creating subscription
            chat_subscription = ChChatSubscription(chat=chat, profile=profile)
            chat_subscription.save()
            hive_subscription = ChHiveSubscription(hive=hive, profile=profile)
            hive_subscription.save()

            # return HttpResponseRedirect("/create_hive/create/")
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "core/create_hive.html", {
            'formHive': formHive,
            'formTags': formTags
        })


@login_required
def create_community(request):
    """
    :param request:
    :return: Web page with the form for creating a hive
    """
    if request.method == 'POST':
        formCommunity = CreateHiveForm(request.POST, prefix='formHive')
        formCommunityTags = TagForm(request.POST, prefix='formTags')
        if formCommunity.is_valid() and formCommunityTags.is_valid():
            user = request.user
            profile = ChProfile.objects.get(user=user)

            # transaction.set_autocommit(False)

            hive_name = formCommunity.cleaned_data['name']
            hive = formCommunity.save(commit=False)
            hive.creator = profile
            hive.name_url = hive_name.replace(" ", "_")
            hive.name_url = replace_unicode(hive.name_url)
            hive.type = 'Community'

            try:
                ChHive.objects.get(name_url=hive.name_url)
                return HttpResponse("This hive already exists")
            except ChHive.DoesNotExist:
                # hive.name_url = replace_unicode(hive_name)
                hive.save()

            # Adding tags
            tagsText = formCommunityTags.cleaned_data['tags']
            tagsArray = tagsText.split(" ")
            hive.set_tags(tagsArray)
            hive.save()

            # Creating community from hive
            community = ChCommunity(hive=hive, admin=profile)
            community.save()

            # Creating subscription
            subscription = ChHiveSubscription(hive=hive, profile=profile)
            subscription.save()

            # Creating public chat of hive
            community.new_public_chat(name=hive.name, description=hive.description)

            # return HttpResponseRedirect("/create_hive/create/")
            # transaction.set_autocommit(True)
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "core/create_community.html", {
            'formHive': formHive,
            'formTags': formTags
        })


@login_required
def create_chat(request, hive_url, public_name):
    """
    :param request:
    :return: Web page with the form for creating a hive
    """
    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        invited = ChProfile.objects.get(public_name=public_name)
        hive = ChHive.objects.get(name_url=hive_url)
        if profile == invited:
            raise Http404

        profile_subscriptions = ChChatSubscription.objects.select_related().filter(profile=profile)
        invited_subscription = ChChatSubscription.objects.none()
        if profile_subscriptions:
            for profile_subscription in profile_subscriptions:
                try:
                    if profile_subscription.chat and profile_subscription.chat.type == 'private':
                        invited_subscription = profile_subscription.chat.chat_subscription.get(profile=invited)
                except profile_subscription.DoesNotExist:
                    continue

        if not invited_subscription:
            # Creating private chat
            chat = ChChat()
            chat.hive = hive
            chat.type = 'private'
            # chat.channel = replace_unicode(profile.public_name + "_" + invited.public_name + "_" + hive_url)
            chat.save()

            subscription1 = ChChatSubscription(chat=chat, profile=profile)
            subscription1.save()
            subscription2 = ChChatSubscription(chat=chat, profile=invited)
            subscription2.save()

            return HttpResponseRedirect("/chat/" + chat.channel_unicode)
        else:
            return HttpResponseRedirect("/chat/" + invited_subscription.chat.channel_unicode)
    else:
        raise Http404


@login_required
def create_public_chat(request, hive_url):
    """
    :param request:
    :return: Web page with the form for creating a new public chat
    """
    if request.method == 'POST':
        form = CreateCommunityChatForm(request.POST)
        if form.is_valid():
            hive = ChHive.objects.get(name_url=hive_url)
            community = ChCommunity.objects.get(hive=hive)
            community.new_public_chat(form.cleaned_data['name'], form.cleaned_data['description'])
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateCommunityChatForm
        hive = ChHive.objects.get(name_url=hive_url)
        return render(request, "core/create_public_chat.html", {
            'form': form,
            'hive': hive
        })


@login_required
def join(request, hive_url):
    """
    :param request:
    :param hive_name: Name of the hive that will be joined to
    :return: Home web page with the subscription created
    """
    if request.method == 'GET':
        # Getting needed information
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive_joining = ChHive.objects.get(name_url=hive_url)

        hive_joining.join(profile)

        return HttpResponseRedirect('/home/')
    else:
        raise Http404


@login_required
def leave(request, hive_url):
    """
    :param request:
    :param hive_url:
    :return:
    """
    if request.method == 'GET':
        # Getting needed information
        username = request.user
        # user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=username)
        hive_leaving = ChHive.objects.get(name_url=hive_url)

        hive_leaving.leave(profile)

        return HttpResponseRedirect("/home/")
    else:
        raise Http404


@login_required
def hives(request):
    """
    :param request:
    :return: Home web page
    """
    if request.method == 'GET':
        # Getting needed info
        user = request.user
        profile = user.profile

        # Trying to get all the subscriptions of this profile
        try:
            hives = profile.hives
        except ChHiveSubscription.DoesNotExist:
            return HttpResponse("Subscription not found")
        return render(request, "core/home_hives.html", {
            'hives': hives
        })


@login_required
def chats(request):
    if request.method == 'GET':
        user = request.user
        profile = user.profile

        try:
            chats = profile.chats
        except ChChatSubscription.DoesNotExist:
            return HttpResponse("Subscription not found")

        return render(request, "core/home_chats.html", {
            'chats': chats
        })

    else:
        raise Http404


@login_required
def explore(request):
    """
    :param request:
    :return: Explore web page which contains all hives
    """
    if request.method == 'GET':
        # Returns all the hives (subscribed and not subscribed)
        try:
            hives = ChHive.objects.all()
        except ChHive.DoesNotExist:
            hives = None
        return render(request, "core/explore.html", {
            'hives': hives
        })


@login_required
def profile(request, public_name, private):
    """
    :param request:
    :param private: Type of profile which is going to be shown, private or public
    :return: Profile web page which contains your personal info
    """
    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        if public_name != profile.public_name and private == 'private':
            raise Http404
        else:
            try:
                if public_name == 'my_profile' or public_name == profile.public_name:
                    profile_view = profile
                    allowed = True
                else:
                    profile_view = ChProfile.objects.get(public_name=public_name)
                    allowed = False
            except ChProfile.DoesNotExist:
                raise Http404
            if private == "private":
                data = {"public_name": profile_view.public_name,
                        "first_name": profile_view.first_name,
                        "birth_date": profile_view.birth_date,
                        "surname": profile_view.last_name,
                        "sex": profile_view.sex,
                        "username": profile.username,
                        "allowed": allowed
                }
                languages = profile.languages
                return render(request, "core/private_profile.html", {
                    "profile": data,
                    "languages": languages
                })
            elif private == "public":
                data = {"public_name": profile_view.public_name,
                        "location": profile_view.location,
                        "show_age": profile_view.public_show_age,
                        "allowed": allowed
                }
                languages = profile.languages
                return render(request, "core/public_profile.html", {
                    "profile": data,
                    "languages": languages
                })
            else:
                return HttpResponse("Error")
    else:
        raise Http404


@login_required
def chat(request, chat_url):
    """
    :param request:
    :param chat_url: Url of the chat
    :return: Chat web page which allows to chat with users who joined the same channel
    """
    # info retrieval
    user = request.user
    profile = ChProfile.objects.get(user=user)
    chat = ChChat.objects.get(channel_unicode=chat_url)
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'

    # GET vs POST
    if request.method == 'POST':
        try:
            ChChatSubscription.objects.get(profile=profile, chat=chat)
            msg = request.POST.get("message")
            timestamp = request.POST.get("timestamp")
            message = chat.new_message(profile=profile,
                                       content_type='text',
                                       content=msg,
                                       timestamp=timestamp)
            chat.save()

            json_message = json.dumps({"username": user.username,
                                       "public_name": profile.public_name,
                                       "message": msg,
                                       "timestamp": timestamp,
                                       "server_time": message.datetime.astimezone()},
                                      cls=DjangoJSONEncoder)

            try:
                chat.send_message(profile=profile, json_message=json_message)
            except AndroidDevice.DoesNotExist:
                return HttpResponse("Not delivered")

            # json_chats = json.dumps([{"CHANNEL": "presence-3240aa0fe3ca15051680641a59e8d7b61c286b23",
            #                           "MESSAGE_ID_LIST": [1, 2, 3, 4, 5]}])
            # ChChat.confirm_messages(json_chats, profile)

            return HttpResponse("Server Ok")

        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response
    # GET
    else:
        try:
            ChChatSubscription.objects.get(chat=chat, profile=profile)

            form = MsgForm()
            return render(request, "core/chat.html", {
                'user': user.username,
                'hive': chat.hive,
                'app_key': app_key,
                'key': key,
                'url': chat_url,
                'channel': chat.channel_unicode,
                'event': event,
                'form': form,
            })

        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response


@login_required
def hive(request, hive_url):
    """
    :param request:
    :param hive_url: Url of the hive, which will be used for the query
    :return: hive view with users and public chat link
    """

    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive = ChHive.objects.get(name_url=hive_url)
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile)
            chats = ChChat.objects.filter(hive=hive, type='public')
            return render(request, "core/hive.html", {
                'hive': hive,
                'chats': chats,
            })
        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response

    else:
        raise Http404


@login_required
def hive_description(request, hive_url):
    """
    :param request:
    :param hive_url: Url of the hive, which will be used for the query
    :return: hive view with users and public chat link
    """
    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive = ChHive.objects.get(name_url=hive_url)
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile)
            subscribed = True
            ChCommunity.objects.get(hive=hive, admin=profile)
            owner = True
        except ChHiveSubscription.DoesNotExist:
            subscribed = False
            owner = False
        except ChCommunity.DoesNotExist:
            subscribed = True
            owner = False

        return render(request, "core/hive_description.html", {
            'hive': hive,
            'subscribed': subscribed,
            'owner': owner,
        })
 
    else:
        raise Http404


@login_required
def get_hive_users(request, hive_url, init, interval):
    """
    :param request:
    :param hive_url: Url of the hive, which will be used for the query
    :param init: ID of the first message to return
    :param interval: Number of messages to return
    :return: *interval* users from *init*
    """
    if request.method == 'GET':
        hive = ChHive.objects.get(name_url=hive_url)
        profile = request.user.profile
        try:
            profiles = []
            for hive_user in hive.get_users_recommended(profile):
                profiles.append({"public_name": hive_user.public_name})
            return HttpResponse(json.dumps(profiles, cls=DjangoJSONEncoder))

        except ChHiveSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response
    else:
        raise Http404


@login_required
def get_messages(request, chat_name, init, interval):
    """
    :param request:
    :param chat_name: Url of the chat, which will be used for the query
    :param init: ID of the first message to return
    :param interval: Number of messages to return
    :return: *interval* messages from *init*
    """

    # GET vs POST
    if request.method == 'GET':

        # info retrieval
        user = request.user
        profile = ChProfile.objects.get(user=user)
        chat = ChChat.objects.get(channel_unicode=chat_name)

        try:
            ChChatSubscription.objects.get(profile=profile, chat=chat)
            if init == 'last':
                messages = ChMessage.objects.filter(chat=chat).order_by('-_id')[0:int(interval)]
            elif init.isnumeric():
                messages = ChMessage.objects.filter(chat=chat, _id__lte=int(init)).order_by('-_id')[0:int(interval)]
            else:
                raise Http404
            messages_row = []
            for message in messages:
                messages_row.append({"username": message.profile.username,
                                     "public_name": message.profile.public_name,
                                     "message": message.content,
                                     "timestamp": message.client_datetime,
                                     "server_time": message.datetime.astimezone(),
                                     "id": message.id
                })
            return HttpResponse(json.dumps(messages_row, cls=DjangoJSONEncoder))
        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response
    else:
        raise Http404


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


def android_test(request):
    return render(request, "core/android_test.html")


def test(request):
    if request.method == 'POST':
        data = request.POST.items()
        headers = request.POST.get("head")
    if request.method == 'GET':
        data = request.GET.items()
        headers = request.GET.get("head")
    return HttpResponse(headers)