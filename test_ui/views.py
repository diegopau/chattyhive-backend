from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.models import *
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from slugify import slugify
from django.db import transaction
from django.db.models import Q
from chattyhive_project.settings import common_settings

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
                hive.slug = slugify(hive_name, translate=None, to_lower=True, separator='-', capitalize=False, max_length=250)
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
                chat.slug = chat.chat_id + '-' + hive.slug
                chat.save()

                # Creating public chat of hive, step 2: ChPublicChat object
                public_chat = ChPublicChat(chat=chat, hive=hive)
                public_chat.slug = slugify(hive_name, translate=None, to_lower=True, separator='-', capitalize=False,
                                           max_length=250)
                public_chat.save()

                # Creating subscription
                hive_subscription = ChHiveSubscription(hive=hive, profile=profile)
                hive_subscription.save()

            # return HttpResponseRedirect("/create_hive/create/")
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=common_settings.TEST_UI_BASE_URL))
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "{app_name}/create_hive.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'formHive': formHive,
            'formTags': formTags,
            'profile': request.user.profile,
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
            hive.slug = slugify(hive_name, translate=None, to_lower=True, separator='-', capitalize=False,
                                max_length=250)
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

            # Adding languages
            hive.languages = formCommunity.cleaned_data['_languages']
            hive.save()

            # Creating community from hive
            community = ChCommunity(hive=hive, owner=profile)
            community.save()

            # Creating subscription
            subscription = ChHiveSubscription(hive=hive, profile=profile)
            subscription.save()

            # Creating public chat of hive
            community.new_public_chat(name=hive.name, public_chat_slug_ending=hive.slug, description=hive.description)

            # return HttpResponseRedirect("/create_hive/create/")
            # transaction.set_autocommit(True)
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=common_settings.TEST_UI_BASE_URL))
        else:
            print("errores formulario community:", formCommunity.errors)
            print(formCommunityTags.errors)
            return HttpResponse("ERROR, invalid form")
    else:
        formHive = CreateHiveForm(prefix="formHive")
        formTags = TagForm(prefix="formTags")
        return render(request, "{app_name}/create_community.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'formHive': formHive,
            'formTags': formTags,
            'profile': request.user.profile,
        })


@login_required
def open_private_chat(request, target_public_name):
    """
    :param request:
    :return: if the chat was already created it just redirects, if not it provides a new chat_id and redirects.
    """
    if request.method == 'GET':
        hive_slug = request.GET.get('hive_slug', '')
        user = request.user
        profile = ChProfile.objects.get(user=user)
        other_profile = ChProfile.objects.get(public_name=target_public_name)
        if profile == other_profile:
            raise Http404

        if hive_slug == '':
            # TODO: for private chats between friends
            pass
        else:
            # Its a private chat inside a hive
            hive = ChHive.objects.get(slug=hive_slug)

            # The user has to be subscribed to the hive in other to chat with other users
            try:
                ChHiveSubscription.objects.get(profile=profile, hive=hive, subscription_state='active')
            except ChHiveSubscription:
                response = HttpResponse("Forbidden")
                response.status_code = 403
                return response
            public_names = sorted([profile.public_name, other_profile.public_name], key=str.lower)
            slug_ends_with = '-' + hive_slug + '--' + public_names[0] + '-' + public_names[1]
            # We try to get the chat object that involves both users
            # for this we use the last part of the slug in the ChChat objects
            try:
                chat = ChChat.objects.get(hive=hive, slug__endswith=slug_ends_with, deleted=False)
            except ChChat.DoesNotExist:
                # If the chat doesn't exist we give a provisional chat_id and redirect:
                chat_id = ChChat.get_chat_id()
                chat_id += slug_ends_with
                return HttpResponseRedirect("/{base_url}/chat/".format(base_url=common_settings.TEST_UI_BASE_URL)
                                            + hive.slug + "/" + chat_id + "?new_chat=True")

            # If the chat exists (and even if it is marked as deleted) we give the chat_id and redirect:
            return HttpResponseRedirect("/{base_url}/chat/".format(
                base_url=common_settings.TEST_UI_BASE_URL) + hive.slug + "/" + chat.chat_id + "?new_chat=False")


@login_required
def chat(request, hive_slug, chat_id):
    """
    :param request:
    :param chat_id: id of the chat
    :return: Chat web page which allows to chat with users who joined the same channel
    """
    # info retrieval
    user = request.user
    hive = ChHive.objects.get(slug=hive_slug)
    profile = ChProfile.objects.get(user=user)
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    event = 'msg'

    # POST: User send a new message inside the chat
    if request.method == 'POST':
        message_data = {'profile': profile}
        # We first check if the user is authorized to enter this chat (he must be subscribed to the hive)
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile, subscription_state='active')
        except ChHiveSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response

        new_chat = request.POST.get('new_chat', 'False')
        if new_chat == 'True':
            chat_slug = chat_id

            if chat_slug.find('-') == -1:  # new_chat == True and a chat_id without a slug format shouldn't happen
                response = HttpResponse("Bad request")
                response.status_code = 400
                return response
            else:
                if chat_slug.find('+') != -1:  # This is a chat between friends
                    pass  # TODO
                elif chat_slug.find('--') != -1:  # This is a chat between hivemates inside a hive
                    # We get a chat_id
                    slug_ends_with = chat_slug[chat_slug.find('-'):len(chat_slug)]
                    chat_id = chat_slug[0:chat_slug.find('-')]
                    hive_slug = slug_ends_with[1:slug_ends_with.find('--')]
                    other_profile_public_name = \
                        slug_ends_with.replace(hive_slug, '').replace(profile.public_name, '').replace('-', '')

                    hive = ChHive.objects.get(slug=hive_slug)
                    # We now check if the user is authorized to enter this chat (he must be subscribed to the hive)
                    try:
                        with transaction.atomic():
                            hive_subscription = ChHiveSubscription.objects.select_related().get(
                                hive=hive, profile=profile, subscription_state='active')
                    except ChHiveSubscription.DoesNotExist:
                        response = HttpResponse("Forbidden")
                        response.status_code = 403
                        return response

                    # We search for any other ChChat object with the same ending. Just in case the other profile was also
                    # starting a new chat (he/she would have a different temporal chat_id assigned).
                    try:
                        with transaction.atomic():
                            chat = ChChat.objects.get(hive=hive, slug__endswith=slug_ends_with)
                    except ChChat.DoesNotExist:
                        chat = ChChat(chat_id=chat_id, slug=chat_slug, type='mate_private', hive=hive)
                        chat.save()
                else:  # This could be a public chat
                    response = HttpResponse("Wrong slug, or public chat and new=True incompatible")
                    response.status_code = 400
                    return response
        else:  # new_chat == False
            try:
                chat = ChChat.objects.get(chat_id=chat_id)
                if chat.slug.find('+') != -1:  # This is a chat between friends
                    pass  # TODO
                elif chat.slug.find('--') != -1:  # This is a chat between hivemates inside a hive
                    slug_ends_with = chat.slug[chat.slug.find('-'):len(chat.slug)]
                    hive_slug = slug_ends_with[1:slug_ends_with.find('--')]
                    other_profile_public_name = \
                        slug_ends_with.replace(hive_slug, '').replace(profile.public_name, '').replace('-', '')
                    hive = ChHive.objects.get(slug=hive_slug)
                    # We now check if the user is authorized to enter this chat (he must be subscribed to the hive)
                    try:
                        with transaction.atomic():
                            hive_subscription = \
                                ChHiveSubscription.objects.select_related().get(hive=hive,
                                                                                profile=profile,
                                                                                subscription_state='active')

                    except ChHiveSubscription.DoesNotExist:
                        response = HttpResponse("Forbidden")
                        response.status_code = 403
                        return response

                else:  # This is a public chat
                    hive = chat.hive
                    try:
                        with transaction.atomic():
                            hive_subscription = \
                                ChHiveSubscription.objects.select_related().get(hive=hive,
                                                                                profile=profile,
                                                                                subscription_state='active')
                    except ChHiveSubscription.DoesNotExist:
                        response = HttpResponse("Forbidden")
                        response.status_code = 403
                        return response

            except ChChat.DoesNotExist:
                response = HttpResponse("Unauthorized")
                response.status_code = 401
                return response

        # If the chat exist, then we have to send the message to the existing chat
        if chat.type == 'public':
            pass
        else:  # This is only needed if chat is private
            other_profile = ChProfile.objects.get(public_name=other_profile_public_name)
            message_data['other_profile'] = other_profile
            if chat.deleted:
                chat.deleted = False
                chat.date = timezone.now()
            slug_ends_with = chat.slug[chat.slug.find('-'):len(chat.slug)]
            other_profile_public_name = slug_ends_with.replace(hive_slug, '').replace(profile.public_name, '').replace('-', '')
            try:
                ChChatSubscription.objects.get(
                    chat=chat, profile__public_name=other_profile_public_name)
            except ChChatSubscription.DoesNotExist:
                chat_subscription_other_profile = ChChatSubscription(chat=chat, profile=other_profile)
                chat_subscription_other_profile.save()
        try:
            with transaction.atomic():
                chat_subscription_profile = ChChatSubscription.objects.get(chat=chat, profile=profile)
                if chat_subscription_profile.subscription_state == 'deleted':
                    chat_subscription_profile.subscription_state = 'active'
                    chat_subscription_profile.save()
        except ChChatSubscription.DoesNotExist:
            chat_subscription_profile = ChChatSubscription(chat=chat, profile=profile)
            chat_subscription_profile.save()

        msg = request.POST.get("message")
        message = chat.new_message(profile=profile,
                                   content_type='text',
                                   content=msg,)
        chat.save()
        chat_subscription_profile.profile_last_activity = timezone.now()
        chat_subscription_profile.save()
        if chat.type == 'public':
            hive_subscription.profile_last_activity = timezone.now()
            hive_subscription.save()

        message_data['socket_id'] = request.POST.get("socket_id")
        if new_chat.lower() == 'true':
            message_chat_id = chat_slug
        else:
            message_chat_id = chat_id

        message_data['json_message'] = json.dumps({"chat_id": message_chat_id,
                                                   "message_id": message.id,
                                                   "public_name": profile.public_name,
                                                   "content": msg,
                                                   "server_time": message.created.astimezone()},
                                                  cls=DjangoJSONEncoder)

        try:
            chat.send_message(message_data)
        except Device.DoesNotExist:
            return HttpResponse("Not delivered")
        return HttpResponse("Server Ok")

    # GET: User retrieve the chat messages
    else:
        # We first check if the user is authorized to enter this chat (he must be subscribed to the hive)
        try:
            ChHiveSubscription.objects.get(hive=hive, profile=profile, subscription_state='active')
        except ChHiveSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response

        new_chat = request.GET.get('new_chat', False)

        if not new_chat:
            # We try now to get the chat object, if new_chat==True we don't need to check this
            try:
                chat = ChChat.objects.get(chat_id=chat_id)
            except ChChat.DoesNotExist:
                # The client expected the chat to exist with this chat_id, but it doesn't exist.
                response = HttpResponse("Unauthorized")
                response.status_code = 401
                return response

        form = MsgForm()
        return render(request, "{app_name}/chat.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'user_public_name': user.profile.public_name,
            'hive': hive,
            'app_key': app_key,
            'key': key,
            'url': chat_id,
            'channel': chat_id,
            'event': event,
            'form': form,
            'new_chat': new_chat,
        })


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
        if chat_name.find('-') == -1:
            chat = ChChat.objects.get(chat_id=chat_name)
        else:
            # This is for the case that this is a new private chat or the first message in a private chat
            # has just been sent
            chat_id = chat_name[0:chat_name.find('-')]
            try:
                chat = ChChat.objects.get(chat_id=chat_id)
            except ChChat.DoesNotExist:
                # If the chat doesn't exist we just return no messages
                messages_row = []
                return HttpResponse(json.dumps(messages_row, cls=DjangoJSONEncoder))
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
                                     "content": message.content,
                                     "server_time": message.created.astimezone(),
                                     "id": message.id
                                     })
            return HttpResponse(json.dumps(messages_row, cls=DjangoJSONEncoder))
        except ChChatSubscription.DoesNotExist:
            response = HttpResponse("Unauthorized")
            response.status_code = 401
            return response
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
            public_chat_slug_ending = slugify(form.cleaned_data['name'], translate=None, to_lower=True, separator='-', capitalize=False,
                                              max_length=250)
            community.new_public_chat(form.cleaned_data['name'], public_chat_slug_ending, form.cleaned_data['description'])
            return HttpResponseRedirect("/{base_url}/home/".format(base_url=common_settings.TEST_UI_BASE_URL))
        else:
            return HttpResponse("ERROR, invalid form")
    else:
        form = CreateCommunityPublicChatForm
        hive = ChHive.objects.get(slug=hive_slug)
        return render(request, "{app_name}/create_public_chat.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'form': form,
            'hive': hive,
            'profile': request.user.profile,
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

        return HttpResponseRedirect('/{base_url}/home/'.format(base_url=common_settings.TEST_UI_BASE_URL))
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

        return HttpResponseRedirect('/{base_url}/home/'.format(base_url=common_settings.TEST_UI_BASE_URL))
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
        profile = request.user.profile

        # Trying to get all the subscriptions of this profile
        try:
            hives = profile.hives
        except ChHiveSubscription.DoesNotExist:
            return HttpResponse("Subscription not found")
        return render(request, "{app_name}/home_hives.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'hives': hives,
            'profile': request.user.profile,
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

        return render(request, "{app_name}/home_chats.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'chats': chats,
            'profile': profile
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

        # We have to exclude hives that the user is subscribed (and the subscription not marked as deleted)
        user_hive_subscriptions = ChHiveSubscription.objects.filter(profile=request.user.profile, subscription_state='active')

        try:
            hives = ChHive.objects.all().exclude(deleted=True).exclude(subscriptions__in=user_hive_subscriptions)
        except ChHive.DoesNotExist:
            hives = None

        return render(request, "{app_name}/explore.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'hives': hives,
            'profile': request.user.profile
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
                return render(request, "{app_name}/private_profile.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
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
                return render(request, "{app_name}/public_profile.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
                    "profile": data,
                    "languages": languages
                })
            else:
                return HttpResponse("Error")
    else:
        raise Http404


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
            return render(request, "{app_name}/hive.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
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
                elif profile in community.admins.all():
                    admin = True
            except ChCommunity.DoesNotExist:
                pass

        except ChHiveSubscription.DoesNotExist:
            pass

        return render(request, "{app_name}/hive_description.html".format(app_name=common_settings.TEST_UI_APP_NAME), {
            'hive': hive,
            'subscribed': subscribed,
            'owner': owner,
            'admin': admin,
            'profile': request.user.profile
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


def android_test(request):
    return render(request, "{app_name}/android_test.html".format(app_name=common_settings.TEST_UI_APP_NAME))


def test(request):
    if request.method == 'POST':
        data = request.POST.items()
        headers = request.POST.get("head")
    if request.method == 'GET':
        data = request.GET.items()
        headers = request.GET.get("head")
    return HttpResponse(headers)
