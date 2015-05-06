from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from slugify import slugify
from django.db import transaction

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
            with transaction.atomic():
                user = request.user
                profile = ChProfile.objects.get(user=user)
                hive_name = formHive.cleaned_data['name']
                hive = formHive.save(commit=False)
                hive.creator = profile
                hive.slug = slugify(hive_name, to_lower=True, separator='-', capitalize=False, max_length=250)
                try:
                    with transaction.atomic():
                        ChHive.objects.get(slug=hive.slug)
                        return HttpResponse("The hive slug already exists")
                except ChHive.DoesNotExist:
                    # hive.slug = replace_unicode(hive_name)
                    hive.save()

                # Adding tags
                tagsText = formTags.cleaned_data['tags']
                tagsList = re.split(r'[, ]+', tagsText)
                hive.set_tags(tagsList)
                hive.save()

                # Adding languages
                hive.languages = formHive.cleaned_data['_languages']
                hive.save()

                # Creating public chat of hive, step 1: ChChat object
                chat = ChChat()
                chat.hive = hive
                chat.type = 'public'
                chat.chat_id = ChChat.get_chat_id()
                chat.save()

                # Creating public chat of hive, step 2: ChPublicChat object
                public_chat = ChPublicChat(chat=chat, hive=hive)
                public_chat.slug = slugify(hive_name, to_lower=True, separator='-', capitalize=False, max_length=250)
                public_chat.save()

                # Creating subscription
                hive_subscription = ChHiveSubscription(hive=hive, profile=profile)
                hive_subscription.save()

            # return HttpResponseRedirect("/create_hive/create/")
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=settings.TEST_UI_BASE_URL))
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "{app_name}/create_hive.html".format(app_name=settings.TEST_UI_APP_NAME), {
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
            hive.slug = hive_name.replace(" ", "-")
            # TODO: se está metiendo como slug el hive_name mal tuneado, esto hay que corregirlo.
            hive.type = 'Community'

            try:
                ChHive.objects.get(slug=hive.slug)
                return HttpResponse("This hive already exists")
            except ChHive.DoesNotExist:
                # hive.slug = replace_unicode(hive_name)
                hive.save()

            # Adding tags
            tagsText = formCommunityTags.cleaned_data['tags']
            tagsList = re.split(r'[, ]+', tagsText)
            hive.set_tags(tagsList)
            hive.save()

            # Creating community from hive
            community = ChCommunity(hive=hive, owner=profile)
            community.save()

            # Creating subscription
            subscription = ChHiveSubscription(hive=hive, profile=profile)
            subscription.save()

            # Creating public chat of hive
            community.new_public_chat(name=hive.name, description=hive.description)

            # return HttpResponseRedirect("/create_hive/create/")
            # transaction.set_autocommit(True)
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=settings.TEST_UI_BASE_URL))
        else:
            print("errores formulario community:", formCommunity.errors)
            print(formCommunityTags.errors)
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "{app_name}/create_community.html".format(app_name=settings.TEST_UI_APP_NAME), {
            'formHive': formHive,
            'formTags': formTags
        })


@login_required
def open_hive_private_chat(request, hive_slug, public_name):
    """
    :param request:
    :return: if the chat was already created it just redirects, if not it provides a new chat_id and redirects.
    """
    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        other_profile = ChProfile.objects.get(public_name=public_name)
        hive = ChHive.objects.get(slug=hive_slug)
        if profile == other_profile:
            raise Http404

        # We try to get the chat object that involves both users
        # try:
        #     chat = ChChat.objects.get(chat_subscribers__in=[profile, other_profile])
        #
        # # We get every private chat subscription of the user for this hive/community
        # profile_subscriptions = ChChatSubscription.objects.select_related('chat').filter(profile=profile,
        #                                                                                  chat__hive=hive,
        #                                                                                  chat__type='mate_private')

        # other_profile_subscription = ChChatSubscription.objects.none()
        #
        # if profile_subscriptions:
        #     for subscription in profile_subscriptions:
        #         try:
        #             # We check, for every chat subscription of the user if the other user is also subscribed
        #             other_profile_subscription = subscription.chat.chat_subscribers.get(profile=other_profile)
        #
        # else:
        #
        # if profile_subscriptions:
        #     for profile_subscription in profile_subscriptions:
        #         try:
        #             # For each private chat subscription of the user
        #             if profile_subscription.chat:
        #                 # we check if the other user is also
        #                 other_profile_subscription = profile_subscription.chat.chat_subscribers.get(
        #                     profile=other_profile)
        #         except profile_subscription.DoesNotExist:
        #             continue
        #
        # if not other_profile_subscription:
        #     # Creating private chat
        #     chat = ChChat()
        #     chat.hive = hive
        #     chat.type = 'mate_private'
        #     chat.chat_id = ChChat.get_chat_id()
        #     chat.save()
        #
        #     subscription_user = ChChatSubscription(chat=chat, profile=profile)
        #     subscription_user.save()
        #     subscription_other_user = ChChatSubscription(chat=chat, profile=other_profile)
        #     subscription_other_user.save()
        #
        #     return HttpResponseRedirect("/{base_url}/chat/".format(base_url=settings.TEST_UI_BASE_URL)
        #                                 + ct_idunicode)
        # else:
        #     return HttpResponseRedirect("/{base_url}/chat/".format(base_url=settings.TEST_UI_BASE_URL)
        #                                 + other_profile_subscription.ct_idunicode)
    else:
        raise Http404


@login_required
def create_public_chat(request, hive_slug):
    """
    :param request:
    :return: Web page with the form for creating a new public chat
    """
    if request.method == 'POST':
        form = CreateCommunityPublicChatForm(request.POST)
        if form.is_valid():
            hive = ChHive.objects.get(slug=hive_slug)
            community = ChCommunity.objects.get(hive=hive)
            public_chat_slug = slugify(hive.name, to_lower=True, separator='-', capitalize=False, max_length=250)
            community.new_public_chat(form.cleaned_data['name'], form.cleaned_data['description'],
                                      slug=public_chat_slug)
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=settings.TEST_UI_BASE_URL))
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateCommunityPublicChatForm
        hive = ChHive.objects.get(slug=hive_slug)
        return render(request, "{app_name}/create_public_chat.html".format(app_name=settings.TEST_UI_APP_NAME), {
            'form': form,
            'hive': hive
        })


@login_required
def join(request, hive_slug):
    """
    :param request:
    :param hive_name: Name of the hive that will be joined to
    :return: Home web page with the subscription created
    """
    if request.method == 'GET':
        # Getting needed information
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive_joining = ChHive.objects.get(slug=hive_slug)

        hive_joining.join(profile)

        return HttpResponseRedirect('/{base_url}/home/'.format(base_url=settings.TEST_UI_BASE_URL))
    else:
        raise Http404


@login_required
def leave(request, hive_slug):
    """
    :param request:
    :param hive_slug:
    :return:
    """
    if request.method == 'GET':
        # Getting needed information
        username = request.user
        # user = ChUser.objects.get(username=username)
        profile = ChProfile.objects.get(user=username)
        hive_leaving = ChHive.objects.get(slug=hive_slug)

        hive_leaving.leave(profile)

        return HttpResponseRedirect('/{base_url}/home/'.format(base_url=settings.TEST_UI_BASE_URL))
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
        return render(request, "{app_name}/home_hives.html".format(app_name=settings.TEST_UI_APP_NAME), {
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

        return render(request, "{app_name}/home_chats.html".format(app_name=settings.TEST_UI_APP_NAME), {
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
            hives = ChHive.objects.all().exclude(deleted=True)

        except ChHive.DoesNotExist:
            hives = None
        return render(request, "{app_name}/explore.html".format(app_name=settings.TEST_UI_APP_NAME), {
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
                        "location": profile.display_location(),
                        "allowed": allowed
                        }
                languages = profile.languages
                return render(request, "{app_name}/private_profile.html".format(app_name=settings.TEST_UI_APP_NAME), {
                    "profile": data,
                    "languages": languages
                })
            elif private == "public":
                data = {"public_name": profile_view.public_name,
                        "location": profile_view.display_location(),
                        "show_age": profile_view.public_show_age,
                        "allowed": allowed
                        }
                languages = profile.languages
                return render(request, "{app_name}/public_profile.html".format(app_name=settings.TEST_UI_APP_NAME), {
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
    chat = ChChat.objects.get(chat_id=chat_url)
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
            except Device.DoesNotExist:
                return HttpResponse("Not delivered")

            # json_chats = json.dumps([{"CHANNEL": "presence-3240aa0fe3ca15051680641a59e8d7b61c286b23",
            # "MESSAGE_ID_LIST": [1, 2, 3, 4, 5]}])
            # ChChat.confirm_messages(json_chats, profile)

            return HttpResponse("Server Ok")

        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response
    # GET
    else:
        try:
            ChChatSubscription.objects.get(chat=chat, profile=profile, deleted=False)

        except ChChatSubscription.DoesNotExist:
            # If the subscription was not found might be one of two things:
            # 1. The user can chat but its the first time the user chats with this other user, or in the public chat,
            # so we must create a ChChatSubscription for him.
            # 2. The client is trying to access to a chat he is not allowed to. In this case he is not authorized.
            # TODO: If in the future we have restricted public chats, we have to make additional checkings here

            try:
                ChHiveSubscription.objects.get(hive=chat.hive, profile=profile, deleted=False)
                # If the user is subscribed to the hive but he didn't have a ChChatSubscription for this chat, then the
                # user is just opening this chat for the first time. We add it to his chat list.
                chat_subscription = ChChatSubscription(chat=chat, profile=profile)
                chat_subscription.save()

            except ChHiveSubscription.DoesNotExist:
                response = HttpResponse("Unauthorized")
                response.status_code = 401
                return response

        form = MsgForm()
        return render(request, "{app_name}/chat.html".format(app_name=settings.TEST_UI_APP_NAME), {
            'user': user.username,
            'hive': chat.hive,
            'app_key': app_key,
            'key': key,
            'url': chat_url,
            'channel': chat.chat_id,
            'event': event,
            'form': form,
        })

@login_required
def hive(request, hive_slug):
    """
    :param request:
    :param hive_slug: Url of the hive, which will be used for the query
    :return: hive view with users and public chat link
    """

    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive = ChHive.objects.get(slug=hive_slug)
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile)
            chats = ChChat.objects.filter(hive=hive, type='public')
            return render(request, "{app_name}/hive.html".format(app_name=settings.TEST_UI_APP_NAME), {
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
def hive_description(request, hive_slug):
    """
    :param request:
    :param hive_slug: Url of the hive, which will be used for the query
    :return: hive view with users and public chat link
    """
    if request.method == 'GET':
        user = request.user
        profile = ChProfile.objects.get(user=user)
        hive = ChHive.objects.get(slug=hive_slug)
        subscribed = False
        owner = False
        admin = False
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile)
            subscribed = True

            try:
                community = ChCommunity.objects.get(hive=hive)
                if community.owner == profile:
                    owner = True
                elif profile in community.admins:
                    admin = True
            except ChCommunity.DoesNotExist:
                pass

        except ChHiveSubscription.DoesNotExist:
            pass

        return render(request, "{app_name}/hive_description.html".format(app_name=settings.TEST_UI_APP_NAME), {
            'hive': hive,
            'subscribed': subscribed,
            'owner': owner,
            'admin': admin,
        })

    else:
        raise Http404


@login_required
def get_hive_users(request, hive_slug, init, interval):
    """
    :param request:
    :param hive_slug: Url of the hive, which will be used for the query
    :param init: ID of the first message to return
    :param interval: Number of messages to return
    :return: *interval* users from *init*
    """
    if request.method == 'GET':
        hive = ChHive.objects.get(slug=hive_slug)
        profile = request.user.profile
        try:
            profiles = []
            print("Perfiles a mostrar: ")
            for hive_user in hive.get_users_recommended(profile):
                print(hive_user.public_name)
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
        chat = ChChat.objects.get(chat_id=chat_name)

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


def android_test(request):
    return render(request, "{app_name}/android_test.html".format(app_name=settings.TEST_UI_APP_NAME))


def test(request):
    if request.method == 'POST':
        data = request.POST.items()
        headers = request.POST.get("head")
    if request.method == 'GET':
        data = request.GET.items()
        headers = request.GET.get("head")
    return HttpResponse(headers)