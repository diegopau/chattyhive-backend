from django.utils import timezone

__author__ = 'diego'

import django
import json
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from core.models import ChUser, ChProfile, ChUserManager, ChChatSubscription, ChHiveSubscription, ChHive, ChChat, \
    ChMessage, Device
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, Http404
import pusher
from email_confirmation.models import EmailAddress, EmailConfirmation
from API import serializers
from API import permissions
from email_confirmation import email_info
import datetime
from django.contrib.auth import authenticate, login, logout
from chattyhive_project import settings
from django.db import IntegrityError, transaction

# =================================================================== #
#                     Django Rest Framework imports                   #
# =================================================================== #

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.exceptions import APIException


# ============================================================ #
#                     Sessions & sync                          #
# ============================================================ #

# TODO: este método podría no ser ni necesario, en principio no está claro que una app para Android necesite csrf.
# También hay que comprobar si el uso de Tokens en autenticación invalida la necesidad de csrf, no sólo para apps
# móviles sino también para navegadores web.
@api_view(['GET'])
@parser_classes((JSONParser,))
def start_session(request, format=None):
    """Returns a csrf cookie
    """
    if request.method == 'GET':
        csrf = django.middleware.csrf.get_token(request)
        data_dict = {'csrf': csrf}
        return Response(data=data_dict, status=status.HTTP_200_OK)



class UserLogin(APIView):

    def get_or_register_device(self, dev_id, dev_type, dev_os, new_device, user):

        # The dev_id should point to an existing device
        if not new_device and (dev_id != ''):
            try:
                device = Device.objects.get(dev_id=dev_id, active=True)
                device.last_login = timezone.now()
                device.save()
                return device.dev_id
            except Device.DoesNotExist:
                return Response({'error_message': 'The device does not exist anymore'}, status=status.HTTP_404_NOT_FOUND)

        # There is no device but we don't have to create one either (request comes from browser or a device without
        # support for notifications
        if not new_device and (dev_id == ''):
            pass
            return dev_id

        if new_device:
            device = Device(active=True, dev_os=dev_os, dev_type=dev_type, last_login=timezone.now(),
                            user=user)
            device.dev_id = Device.get_dev_id()
            device.save()
            return device.dev_id

    def post(self, request, format=None):
        # TODO: The code of this method could be heavily cleaned/optimized
        """POST sessions/login/

        Returns 200 OK if credentials are ok
        """
        data_dict = {}  # This will contain the data to be sent as JSON
        needs_public_name = False
        new_device = False
        temp_dev_id = ''

        if request.user.is_authenticated():  # User was already logged in
            return Response({'error_message': 'The user was already logged in'}, status=status.HTTP_202_ACCEPTED)

        if 'email' in request.data and 'public_name' in request.data:
            print("email and public_name should not be together in the JSON of the same request")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif 'email' in request.data:
            fields_to_allow = ['email', 'password']
            needs_public_name = True
        elif 'public_name' in request.data:
            fields_to_allow = ['public_name', 'password']
        else:
            print("at least email or public_name should be in the JSON")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if ('dev_os' in request.data) and ('dev_type' in request.data):
            if 'dev_id' in request.data:
                print("dev_id, dev_os and dev_type shouldn't be together in the request")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fields_to_allow.append('dev_os')
            fields_to_allow.append('dev_type')
            # If request is coming from a web browser we will not associate any device with it
            if request.data['dev_os'] == 'android':
                new_device = True
            temp_dev_id = ''
        elif 'dev_id' in request.data:
            if ('dev_os' in request.data) or ('dev_type' in request.data):
                print("dev_os or dev_type fields shouldn't be included in this case")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if request.data['dev_id'] == '':
                print("dev_id can't be blank")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fields_to_allow.append('dev_id')
            temp_dev_id = request.data['dev_id']
        else:
            print("some fields are missing, probably dev_type or dev_os")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # fields specifies the fields to be considered by the serializer
        serializer = serializers.LoginCredentialsSerializer(data=request.data, fields=fields_to_allow)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                    email_address = EmailAddress.objects.get(email=user.email)
                    if not email_address.verified:
                        try:
                            user_email_confirmation = EmailConfirmation.objects.get(
                                email_address=EmailAddress.objects.get(email=user.email))
                            if email_address.warned:
                                # THE USER HAS BEEN ALREADY WARNED
                                if user_email_confirmation.warning_expired():
                                    # EXTRA EXPIRATION DATE IS DUE, account is disabled or marked as disabled if
                                    # it wasn't so
                                    data_dict['email_verification'] = 'expired'
                                    EmailAddress.objects.check_confirmation(email_address)
                                    return Response(data_dict, status=status.HTTP_401_UNAUTHORIZED)
                                else:
                                    # FIRST EXPIRATION DATE IS DUE and it has been already checked and warned, but the
                                    # extra warning time has not expired,
                                    # we are in the middle of the extra expiration time
                                    login(request, user)
                                    if new_device:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type=serializer.validated_data['dev_type'],
                                                                        dev_os=serializer.validated_data['dev_os'],
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    data_dict['email_verification'] = 'warned'
                                    if needs_public_name:
                                        data_dict['public_name'] = user.chprofile.public_name
                                    data_dict['expiration_date'] = \
                                        user_email_confirmation.warned_day + datetime.timedelta(
                                            days=email_info.EMAIL_AFTER_WARNING_DAYS)
                                    return Response(data_dict, status=status.HTTP_200_OK)
                            else:
                                # THE USER HAS NOT BEEN ALREADY WARNED
                                if user_email_confirmation.key_expired():
                                    # FIRST EXPIRATION DATE IS DUE and its the first time its been checked
                                    EmailAddress.objects.warn(email_address)
                                    # With login method we persist the authentication, so the client won't have to
                                    # re-authenticate with each request.
                                    login(request, user)
                                    if new_device:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type=serializer.validated_data['dev_type'],
                                                                        dev_os=serializer.validated_data['dev_os'],
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    if needs_public_name:
                                        data_dict['public_name'] = user.chprofile.public_name
                                    data_dict['email_verification'] = 'warn'
                                    data_dict['expiration_date'] = \
                                        user_email_confirmation.warned_day + datetime.timedelta(
                                            days=email_info.EMAIL_AFTER_WARNING_DAYS)
                                    return Response(data_dict, status=status.HTTP_200_OK)
                                else:
                                    # FIRST EXPIRATION DATE IS NOT DUE
                                    login(request, user)
                                    if new_device:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type=serializer.validated_data['dev_type'],
                                                                        dev_os=serializer.validated_data['dev_os'],
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        new_device=new_device,
                                                                        user=request.user)
                                    if needs_public_name:
                                        data_dict['public_name'] = user.chprofile.public_name
                                    data_dict['email_verification'] = 'unverified'
                                    data_dict['expiration_date'] = user_email_confirmation.sent + datetime.timedelta(
                                        days=email_info.EMAIL_CONFIRMATION_DAYS)
                                    return Response(data_dict, status=status.HTTP_200_OK)
                        except EmailConfirmation.DoesNotExist:
                            print("email confirmation object does not exist for user ", user.chprofile.public_name)
                    else:
                        # ACCOUNT IS VERIFIED AND ACTIVE
                        login(request, user)
                        if new_device:
                            data_dict['dev_id'] = \
                                self.get_or_register_device(dev_id=temp_dev_id,
                                                            dev_type=serializer.validated_data['dev_type'],
                                                            dev_os=serializer.validated_data['dev_os'],
                                                            new_device=new_device,
                                                            user=request.user)
                        else:
                            data_dict['dev_id'] = \
                                self.get_or_register_device(dev_id=temp_dev_id,
                                                            dev_type='',
                                                            dev_os='',
                                                            new_device=new_device,
                                                            user=request.user)
                        if needs_public_name:
                            data_dict['public_name'] = user.chprofile.public_name
                            return Response(data_dict, status=status.HTTP_200_OK)
                        else:
                            return Response(data_dict, status=status.HTTP_200_OK)
                else:
                    print("The password is valid, but the account has been disabled!")
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
                return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes(permissions.IsAuthenticated,)
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        request.session['active'] = False
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((permissions.IsAuthenticated,))
def set_asynchronous_services(request):
    if request.method == 'POST':

        serializer = serializers.SetAsyncServices(data=request.data)
        data_dict_pusher = {}
        data_dict_gcm = {}

        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes(permissions.IsAuthenticated,)
def asynchronous_authentication(request):
    if request.method == 'POST':

        serializer = serializers.AsyncAuthSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            chat_channel = serializer.validated_data['channel_name']
            chat_id = chat_channel[9:len(chat_channel)]
            chat = ChChat.objects.get(chat_id=chat_id)
            socket_id = serializer.validated_data['socket_id']
            profile = request.user.profile

            try:
                ChChatSubscription.objects.get(chat=chat, profile=profile)

                channel_data = {
                    'user_id': socket_id,
                    'user_info': {
                        'public_name': profile.public_name,
                    }
                }

                pusher_object = pusher.Pusher(
                    app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_APP_KEY,
                    secret=settings.PUSHER_SECRET,
                    encoder=DjangoJSONEncoder,
                )

                auth_response = pusher_object.authenticate(
                    channel=chat_channel,
                    socket_id=socket_id,
                    custom_data=channel_data
                )

                return Response(json.dumps(auth_response, cls=DjangoJSONEncoder), status=status.HTTP_200_OK)

            except ChChatSubscription.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


# ============================================================ #
#                          Explore                             #
# ============================================================ #

class ChHiveList(APIView):
    """Lists hives in Explora or creates new hive

    User listing is just avaliable from the browsable API, the endpoint is only exposed for a POST with a new user
    (user registration)
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """prueba
        """
        hives = ChHive.objects.all()
        serializer = serializers.ChHiveLevel1Serializer(hives, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """post prueba
        """
        serializer = serializers.ChHiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================ #
#                     Users & Profiles                         #
# ============================================================ #


class ChUserList(APIView):
    """Lists all users or creates new user

    User listing is just avaliable from the browsable API, the endpoint is only exposed for a POST with a new user
    (user registration)
    """

    def get(self, request, format=None):
        """prueba
        """
        users = ChUser.objects.all()
        serializer = serializers.ChUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """post prueba
        """
        serializer = serializers.ChUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChUserDetail(APIView):
    """Show user detail, updates user detail or deletes specific user

    User detail is just avaliable from the browsable API, the endpoint is only exposed for a PUT with a new user
    (user registration)
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            return ChUser.objects.get(username=username)
        except ChUser.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = serializers.ChUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        serializer = serializers.ChUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = self.get_object(username)
        # TODO: aquí donde normalmente se llamaría al método user.delete() yo llamo a delete_account() que entiendo es l
        # lo indicado para borrar de forma limplia el perfil y demás (realmente este método es dar la cuenta de baja!
        # Falta confirmar esto bien
        user.delete_account()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChProfileHiveList(APIView):
    """API method: Hive list

    """
    permission_classes = (permissions.IsAuthenticated, permissions.CanGetHiveList)

    def get_object(self, public_name):
        try:
            return ChProfile.objects.select_related().get(public_name=public_name)
        except ChProfile.DoesNotExist:
            raise Http404

    def get(self, request, public_name, format=None):
        profile = self.get_object(public_name)
        try:
            # If the user is requesting his/her own subscriptions we go on
            self.check_object_permissions(self.request, profile)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)
        hives = profile.hive_subscriptions

        fields_to_remove = ('priority',)
        serializer = serializers.ChHiveLevel1Serializer(hives, fields_to_remove=fields_to_remove, many=True)
        return Response(serializer.data)


class ChProfileChatList(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.CanGetChatList)

    def get_object(self, public_name):
        try:
            return ChProfile.objects.select_related().get(public_name=public_name)
        except ChProfile.DoesNotExist:
            raise Http404

    def get(self, request, public_name, format=None):
        profile = self.get_object(public_name)
        try:
            # If the user is requesting his/her own subscriptions we go on
            self.check_object_permissions(self.request, profile)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)
        chats = profile.chat_subscriptions
        # En fields se le pasa el campo a eliminar del serializador
        serializer = serializers.ChChatListLevel2Serializer(chats, many=True)
        return Response(serializer.data)


class ChProfileDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, public_name):
        try:
            return ChProfile.objects.get(public_name=public_name)
        except ChProfile.DoesNotExist:
            raise Http404

    def get(self, request, public_name, format=None):
        profile = self.get_object(public_name)

        # Como el serializador contiene un HyperlinkedRelatedField, se le tiene que pasar el request a través
        # del contexto
        serializer = serializers.ChProfileLevel1Serializer(profile, context={'request': request})

        return Response(serializer.data)


# ============================================================ #
#                       Hives & Chats                          #
# ============================================================ #

class ChChatDetail(APIView):
    """API method: GET chat info

    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, chat_id):
        try:
            return ChChat.objects.get(chat_id=chat_id)
        except ChChat.DoesNotExist:
            raise Http404

    def get(self, request, chat_id, format=None):
        chat = self.get_object(chat_id)

        serializer = serializers.ChChatLevel3Serializer(chat)

        return Response(serializer.data)


class ChHiveDetail(APIView):
    """API method: GET hive info

    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, hive_slug):
        try:
            return ChHive.objects.get(slug=hive_slug)
        except ChHive.DoesNotExist:
            raise Http404

    def get(self, request, hive_slug, format=None):
        hive = self.get_object(hive_slug)
        fields_to_remove = ('chprofile_set',)
        serializer = serializers.ChHiveSerializer(hive, fields_to_remove=fields_to_remove)

        return Response(serializer.data)


class ChMessageList(APIView):
    """API method: Chat messages

    """
    permission_classes = (permissions.IsAuthenticated, permissions.CanGetChatMessages)

    def get_chat(self, chat_id):
        try:
            return ChChat.objects.get(chat_id=chat_id, deleted=False)
        except ChChat.DoesNotExist:
            raise Http404

    def get(self, request, chat_id, format=None):
        chat = self.get_chat(chat_id)
        try:
            self.check_object_permissions(self.request, chat)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)
        messages = chat.messages
        serializer = serializers.ChMessageSerializer(messages, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, chat_id, format=None):
        """Storage a message in database and send it to any target devices (via pusher, gcm, etc.)

        """
        fields_to_remove = []
        if 'new_chat' not in request.data:
            fields_to_remove.append('new_chat')

        serializer = serializers.SendMessageSerializer(data=request.data, fields_to_remove=fields_to_remove)

        if serializer.is_valid():
            # info retrieval
            new_chat = request.data.get("new_chat", "False")
            profile = request.user.profile

            # Initialization of the message to be sent
            message_data = {'profile': profile}

            if new_chat.lower() == 'true':
                # In this case the client should be actually sending us a temp_id that is the chat slug
                # We extract the relevant info from it:
                chat_slug = chat_id
                if chat_slug.find('-') == -1:  # new_chat == True and a chat_id without a slug format shouldn't happen
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if chat_slug.find('--') == -1:  # This is a chat between friends
                    pass  # TODO
                else:  # This is a chat between hivemates inside a hive
                    slug_ends_with = chat_slug[chat_slug.find('-'):len(chat_slug)]
                    chat_id = chat_slug[0:chat_slug.find('-')]
                    hive_slug = slug_ends_with[1:slug_ends_with.find('--')]
                    other_profile_public_name = \
                        slug_ends_with.replace(hive_slug, '').replace(profile.public_name, '').replace('-', '')

                    hive = ChHive.objects.get(slug=hive_slug)
                    # We now check if the user is authorized to enter this chat (he must be subscribed to the hive)
                    try:
                        with transaction.atomic():
                            ChHiveSubscription.objects.select_related().get(hive=hive, profile=profile, deleted=False)
                    except ChHiveSubscription.DoesNotExist:
                        return Response(status=status.HTTP_403_FORBIDDEN)

                    # We search for any other ChChat object with the same ending. Just in case the other profile was also
                    # starting a new chat (he/she would have a different temporal chat_id assigned).
                    try:
                        with transaction.atomic():
                            chat = ChChat.objects.get(hive=hive, slug__endswith=slug_ends_with)
                    except ChChat.DoesNotExist:
                        chat = ChChat(chat_id=chat_id, slug=chat_slug, type='mate_private', hive=hive)
                        chat.save()
            else:
                try:
                    with transaction.atomic():
                        # TODO: Aditional checks here if chat is between friends (has the user been blocked by the target user?)
                        chat = ChChat.objects.get(chat_id=chat_id)
                        if chat.slug.find('--') == -1:  # This is a chat between friends
                            pass  # TODO
                        else:  # This is a chat between hivemates inside a hive
                            slug_ends_with = chat.slug[chat.slug.find('-'):len(chat.slug)]
                            hive_slug = slug_ends_with[1:slug_ends_with.find('--')]
                            other_profile_public_name = \
                                slug_ends_with.replace(hive_slug, '').replace(profile.public_name, '').replace('-', '')
                            hive = ChHive.objects.get(slug=hive_slug)
                            # We now check if the user is authorized to enter this chat (he must be subscribed to the hive)
                            try:
                                with transaction.atomic():
                                    ChHiveSubscription.objects.select_related().get(hive=hive, profile=profile,
                                                                                    deleted=False)
                            except ChHiveSubscription.DoesNotExist:
                                return Response(status=status.HTTP_403_FORBIDDEN)
                except ChChat.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            # If the chat exist, then we have to send the message to the existing chat
            if chat.type == 'public':
                pass
            else:  # This is only needed if chat is private
                other_profile = ChProfile.objects.get(public_name=other_profile_public_name)
                message_data['other_profile'] = other_profile
                if chat.deleted:
                    chat.deleted = False
                    chat.date = timezone.now()
                try:
                    with transaction.atomic():
                        other_chat_subscription = ChChatSubscription.objects.get(
                            chat=chat, profile__public_name=other_profile_public_name)
                        if other_chat_subscription.deleted:
                            other_chat_subscription.deleted = False
                            other_chat_subscription.save()
                except ChChatSubscription.DoesNotExist:
                    chat_subscription_other_profile = ChChatSubscription(chat=chat, profile=other_profile)
                    chat_subscription_other_profile.save()
            try:
                with transaction.atomic():
                    chat_subscription = ChChatSubscription.objects.get(chat=chat, profile=profile)
                    if chat_subscription.deleted:
                        chat_subscription.deleted = False
                        chat_subscription.save()
            except ChChatSubscription.DoesNotExist:
                chat_subscription_profile = ChChatSubscription(chat=chat, profile=profile)
                chat_subscription_profile.save()

            msg_content = request.data.get("content")
            client_timestamp = request.data.get("client_timestamp")
            message = chat.new_message(profile=profile,
                                       content_type='text',
                                       content=msg_content,
                                       client_timestamp=client_timestamp)
            chat.save()

            message_data['json_message'] = json.dumps({"public_name": profile.public_name,
                                                       "content": msg_content,
                                                       "client_timestamp": client_timestamp,
                                                       "server_time": message.created.astimezone()},
                                                      cls=DjangoJSONEncoder)

            data_dict = {'message_id': message.id, 'server_timestamp': message.created}
            try:
                with transaction.atomic():
                    chat.send_message(message_data)
            except Device.DoesNotExist:
                return Response(data_dict, status=status.HTTP_201_CREATED)
            return Response(data_dict, status=status.HTTP_200_OK)
        else:
            print("serializer errors: ", serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OpenPrivateChat(APIView):
    """API method: Open private chat

    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, target_public_name, format=None):

        hive_slug = request.GET.get('hive_slug', '')
        user = request.user
        profile = ChProfile.objects.get(user=user)
        other_profile = ChProfile.objects.get(public_name=target_public_name)
        if profile == other_profile:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if hive_slug == '':
            # TODO: for private chats between friends
            pass
        else:
            # Its a private chat inside a hive
            hive = ChHive.objects.get(slug=hive_slug)

            # The user has to be subscribed to the hive in other to chat with other users
            try:
                ChHiveSubscription.objects.get(profile=profile, hive=hive, deleted=False)
            except ChHiveSubscription:
                return Response(status=status.HTTP_403_FORBIDDEN)

            data_dict = {}
            public_names = sorted([profile.public_name, target_public_name], key=str.lower)
            slug_ends_with = '-' + hive_slug + '--' + public_names[0] + '-' + public_names[1]

            # We try to get the chat object that involves both users
            # for this we use the last part of the slug in the ChChat objects
            try:
                chat = ChChat.objects.get(hive=hive, slug__endswith=slug_ends_with, deleted=False)
                data_dict['chat_id'] = chat.chat_id
                data_dict['new_chat'] = False
            except ChChat.DoesNotExist:
                # If the chat doesn't exist we give a provisional chat_id and redirect:
                chat_id = ChChat.get_chat_id()
                temp_chat_id = chat_id + slug_ends_with
                data_dict['chat_id'] = temp_chat_id
                data_dict['new_chat'] = True
            # If the chat exists (and even if it is marked as deleted) we give the chat_id and redirect:
            return Response(data_dict, status=status.HTTP_200_OK)


# ============================================================ #
#                            OLD                               #
# ============================================================ #

def email_check(request):
    """
    :param request:
    :return: JSON with status
    """

    if request.method == 'POST':

        # Getting email from POST param
        aux = request.body
        data = json.loads(aux.decode('utf-8'))
        email = data['email']

        username = email
        # print(email + '_ANDROID')  # PRINT

        # Checking already existing user
        try:
            if ChUser.objects.get(username=username) is not None:
                status = "USER_ALREADY_EXISTS"
            else:
                status = "NONE"
        except ObjectDoesNotExist:
            status = "OK"

        return HttpResponse(json.dumps({'status': status}), content_type="application/json")

    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}), content_type="application/json")


def register(request):
    """
    :param request:
    :return: JSON with status and profile
    """

    if request.method == 'POST':

        # Getting all parameters from POST
        aux = request.body
        data = json.loads(aux.decode('utf-8'))

        email = data['email']
        pass1 = data['pass1']
        public_name = data['public_name']
        first_name = data['first_name']
        last_name = data['last_name']
        sex = data['sex']
        language = data['language']
        private_show_age = data['private_show_age']
        location = data['location']
        public_show_age = data['public_show_age']
        show_location = data['show_location']

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
            profile.public_name = public_name
            profile.first_name = first_name
            profile.last_name = last_name
            profile.sex = sex
            profile.language = language
            profile.private_show_age = private_show_age
            profile.public_show_age = public_show_age
            profile.show_location = show_location
            profile.set_approximate_location(location)
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
                'status': status,  # Returning OK status
                'profile': profile_json  # Returning complete Profile
            }))

    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}))


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
            subscriptions = ChChatSubscription.objects.filter(profile=profile)
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
        except ChChatSubscription.DoesNotExist:
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
            subscription = ChChatSubscription()
            subscription.hive = hive_joining
            subscription.profile = profile
            subscription.chat = chat2
            subscription.save()

            status = 'SUBSCRIBED'
            return HttpResponse(json.dumps({'status': status}, cls=DjangoJSONEncoder), content_type="application/json")

        else:
            status = 'ALREADY_SUBSCRIBED'
            return HttpResponse(json.dumps({'status': status}, cls=DjangoJSONEncoder), content_type="application/json")
    else:
        status = "INVALID_METHOD"
        return HttpResponse(json.dumps({'status': status}), content_type="application/json")
        # raise Http404
