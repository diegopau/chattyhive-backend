from django.utils import timezone
import django
import json
import re
from django.contrib.auth import authenticate
from django.core import exceptions as Excep; Excep.ObjectDoesNotExist, Excep.MultipleObjectsReturned,\
                                             Excep.ValidationError
from django.core.validators import validate_email
from core.models import ChUser, ChProfile, ChUserManager, ChChatSubscription, ChHiveSubscription, ChHive, ChChat, \
    ChMessage, Device, ChCategory, City, Region, Country, ChPublicChat, ChCommunity, GuidelinesModel
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
import pusher
from email_confirmation.models import EmailAddress, EmailConfirmation
from API import serializers
from API import permissions
import datetime
from django.contrib.auth import authenticate, login, logout, hashers
from chattyhive_project.settings import common_settings
from django.db import IntegrityError, transaction
from core.models import UnauthorizedException
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from uuid import uuid4
from django.core.cache import cache
from slugify import slugify

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
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError, NotAuthenticated

__author__ = 'diego'

# ============================================================ #
#                       Support methods                        #
# ============================================================ #


# ============================================================ #
#               Sessions & 3rd-party services                  #
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
#TODO: Login does not require csrftoken right now, why?

    def get_or_register_device(self, dev_id, dev_type, dev_os, dev_code, new_device, reg_id, user):

        # The dev_id should point to an existing device
        if not new_device and (dev_id != ''):
            try:
                device = Device.objects.get(dev_id=dev_id, active=True)
                device.last_activity = timezone.now()
                if (device.reg_id != reg_id) and (reg_id != ''):
                    device.reg_id = reg_id
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
            # First we try if for this user there is already a device matching the parameters
            # public_name + dev_os + dev_type + dev_code
            dev_alternative_id = user.profile.public_name + '-' + dev_os + '-' + dev_type + '-' + dev_code
            try:
                device = Device.objects.get(dev_alternative_id=dev_alternative_id, active=True)
            except Device.DoesNotExist:
                device = Device(active=True, dev_os=dev_os, dev_type=dev_type, dev_alternative_id=dev_alternative_id,
                                last_activity=timezone.now(), reg_id=reg_id, user=user)
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

        if ('dev_os' in request.data) and ('dev_type' in request.data) and ('dev_code' in request.data):
            if 'dev_id' in request.data:
                print("dev_id, dev_os, dev_code and dev_type shouldn't be together in the request")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fields_to_allow.append('dev_os')
            fields_to_allow.append('dev_type')
            fields_to_allow.append('dev_code')
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
            print("some fields are missing, probably dev_type, dev_os or dev_code")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        fields_to_allow.append('services')

        # fields specifies the fields to be considered by the serializer
        serializer = serializers.LoginCredentialsSerializer(data=request.data, fields=fields_to_allow)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")

                    reg_id = ''
                    # We get info about async services from the serializer
                    for service in serializer.validated_data['services']:
                        if service['name'] == 'pusher':
                            pass  # TODO: we don't need anything for pusher from the client just yet...
                        if service['name'] == 'gcm':
                            reg_id = service['reg_id']

                    # We now build a json with the server response that will include info the client might need
                    # about asyn services
                    services = [{'name': 'pusher', 'app': common_settings.PUSHER_APP_KEY, 'reg_id': ''}]
                    data_dict['services'] = services

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
                                    return Response(data_dict, status=status.HTTP_403_FORBIDDEN)
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
                                                                        dev_code=serializer.validated_data['dev_code'],
                                                                        new_device=new_device,
                                                                        reg_id=reg_id,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        dev_code='',
                                                                        new_device=new_device,
                                                                        reg_id='',
                                                                        user=request.user)
                                    data_dict['email_verification'] = 'warned'
                                    if needs_public_name:
                                        data_dict['public_name'] = user.profile.public_name
                                    data_dict['expiration_date'] = \
                                        user_email_confirmation.warned_day + datetime.timedelta(
                                            days=common_settings.EMAIL_AFTER_WARNING_DAYS)

                                    # We update last_login date
                                    user.profile.last_activity = timezone.now()
                                    user.profile.save()

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
                                                                        dev_code=serializer.validated_data['dev_code'],
                                                                        new_device=new_device,
                                                                        reg_id=reg_id,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        dev_code='',
                                                                        new_device=new_device,
                                                                        reg_id='',
                                                                        user=request.user)
                                    if needs_public_name:
                                        data_dict['public_name'] = user.profile.public_name
                                    data_dict['email_verification'] = 'warn'
                                    data_dict['expiration_date'] = \
                                        user_email_confirmation.warned_day + datetime.timedelta(
                                            days=common_settings.EMAIL_AFTER_WARNING_DAYS)

                                    # We update last_login date
                                    user.profile.last_activity = timezone.now()
                                    user.profile.save()

                                    return Response(data_dict, status=status.HTTP_200_OK)
                                else:
                                    # FIRST EXPIRATION DATE IS NOT DUE
                                    login(request, user)
                                    if new_device:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type=serializer.validated_data['dev_type'],
                                                                        dev_os=serializer.validated_data['dev_os'],
                                                                        dev_code=serializer.validated_data['dev_code'],
                                                                        new_device=new_device,
                                                                        reg_id=reg_id,
                                                                        user=request.user)
                                    else:
                                        data_dict['dev_id'] = \
                                            self.get_or_register_device(dev_id=temp_dev_id,
                                                                        dev_type='',
                                                                        dev_os='',
                                                                        dev_code='',
                                                                        new_device=new_device,
                                                                        reg_id='',
                                                                        user=request.user)
                                    if needs_public_name:
                                        data_dict['public_name'] = user.profile.public_name
                                    data_dict['email_verification'] = 'unverified'
                                    data_dict['expiration_date'] = user_email_confirmation.sent + datetime.timedelta(
                                        days=common_settings.EMAIL_CONFIRMATION_DAYS)

                                    # We update last_login date
                                    user.profile.last_activity = timezone.now()
                                    user.profile.save()

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
                                                            dev_code=serializer.validated_data['dev_code'],
                                                            new_device=new_device,
                                                            reg_id=reg_id,
                                                            user=request.user)
                        else:
                            data_dict['dev_id'] = \
                                self.get_or_register_device(dev_id=temp_dev_id,
                                                            dev_type='',
                                                            dev_os='',
                                                            dev_code='',
                                                            new_device=new_device,
                                                            reg_id='',
                                                            user=request.user)

                        # We update last_login date
                        user.profile.last_activity = timezone.now()
                        user.profile.save()

                        if needs_public_name:
                            data_dict['public_name'] = user.profile.public_name
                        return Response(data_dict, status=status.HTTP_200_OK)
                else:
                    print("The password is valid, but the account has been disabled!")
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
                return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((permissions.IsAuthenticated,))
def user_logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class CheckAsynchronousServices(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def check_dev_id(self, dev_id, user):
        try:
            device = Device.objects.get(dev_id=dev_id, active=True)
            if not device.user == user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Here could go code to update the dev_id if needed

        return device

    def update_gcm(self, reg_id, device):

        if (device.reg_id != reg_id) and (reg_id != ''):
            device.reg_id = reg_id
            device.save()

        return reg_id

    def post(self, request, format=None):

        serializer = serializers.CheckAsyncServices(data=request.data)

        if serializer.is_valid(raise_exception=True):
            device = self.check_dev_id(serializer.validated_data['dev_id'], request.user)
            response_data = {}

            for service in serializer.validated_data['services']:
                if service['name'] == 'gcm':
                    new_reg_id = self.update_gcm(reg_id=service['reg_id'], device=device)

            # We now build a json with the server response that will include info the client might need
            # about async services
            services = [{'name': 'pusher', 'app': common_settings.PUSHER_APP_KEY, 'reg_id': ''}]
            response_data['services'] = services

            return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((permissions.IsAuthenticated,))
def asynchronous_authentication(request):
    if request.method == 'POST':

        data_to_serialize = request.data

        # TODO: While we have only pusher auth, this is the easiest way to do it, but must be changed in the future
        data_to_serialize['service'] = 'pusher'

        serializer = serializers.AsyncAuthSerializer(data=data_to_serialize)

        if serializer.is_valid(raise_exception=True):
            chat_channel = serializer.validated_data['channel_name']
            chat_id = chat_channel[9:len(chat_channel)]
            chat = ChChat.objects.get(chat_id=chat_id)
            socket_id = serializer.validated_data['socket_id']
            profile = request.user.profile

            if chat.type != 'public':
                try:
                    ChChatSubscription.objects.get(chat=chat, profile=profile)
                except ChChatSubscription.DoesNotExist:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            channel_data = {
                'user_id': socket_id,
                'user_info': {
                    'public_name': profile.public_name,
                }
            }

            pusher_object = pusher.Pusher(
                app_id=common_settings.PUSHER_APP_ID,
                key=common_settings.PUSHER_APP_KEY,
                secret=common_settings.PUSHER_SECRET,
            )

            auth_response = pusher_object.authenticate(
                channel=chat_channel,
                socket_id=socket_id,
                custom_data=channel_data
            )

            return Response(auth_response, status=status.HTTP_200_OK)



@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((permissions.IsAuthenticated,))
def request_upload(request, format=None):
    """Returns a temporary url for the client where it can upload a file
    """
    if request.method == 'GET':

        s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)

        # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
        temp_bucket = s3_connection.get_bucket('temp-eu.chattyhive.com', validate=False)
        s3_object = Key(temp_bucket)  # With this object with can create either folders or files

        """We create an Universally Unique Identifier (RFC4122) using uuid4()."""
        hex_folder_name = uuid4().hex    # 16^32 values low collision probabilities

        while True:
            if cache.add("s3_temp_dir:" + hex_folder_name, request.user.profile.public_name, 1800):
                break
            else:
                hex_folder_name = uuid4().hex    # 16^32 values low collision probabilities

        s3_object.key = hex_folder_name + '/'
        s3_object.set_metadata('ch_public_name', request.user.profile.public_name)
        s3_object.set_contents_from_string('')

        url = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + '.amazonaws.com/'\
              + common_settings.S3_TEMP_BUCKET + '/' + hex_folder_name + '/'

        return Response({"url": url}, status=status.HTTP_200_OK)



# ============================================================ #
#                     Users & Profiles                         #
# ============================================================ #

class EmailCheckSetAndGet(APIView):

    permission_classes = (permissions.IsAuthenticatedForPutOrGet, permissions.CanGetEmail)

    def get_object(self, public_name):
        try:
            if len(public_name) == 32:  # This actually is a username instead of a public_name
                return ChUser.objects.get(username=public_name)
            else:
                return ChUser.objects.get(profile__public_name=public_name)
        except ChUser.DoesNotExist:
            raise Http404

    def get(self, request, public_name='', format=None):  # API method: email get

        user = self.get_object(public_name)
        self.check_permissions(self.request)

        try:
            # If the user is requesting his/her own email
            self.check_object_permissions(self.request, user.profile)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data_dict = {'email': user.email}
        return Response(data=data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):  # API method: Email check

        if 'email' in request.data:
            try:
                validate_email(request.data['email'])
                ChUser.objects.get(email=request.data['email'])
            except Excep.ValidationError:
                return Response({'error_message': 'Email is not well-formed'}, status=status.HTTP_400_BAD_REQUEST)
            except ChUser.DoesNotExist:
                    pass
            else:
                return Response({'error_message': 'There is already a registered user for this email address'},
                                status=status.HTTP_409_CONFLICT)
        else:
            return Response({'error_message': 'Email is not present'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def put(self, request, format=None):  # API method: Email change

        user = request.user
        self.check_permissions(self.request)

        if 'new_email' in request.data:
            try:
                validate_email(request.data['new_email'])
                ChUser.objects.get(email=request.data['new_email'])
            except Excep.ValidationError:
                return Response({'error_message': 'Email is not well-formed'}, status=status.HTTP_400_BAD_REQUEST)
            except ChUser.DoesNotExist:
                if 'password' in request.data:
                    authenticated_user = authenticate(username=user.username, password=request.data['password'])
                    if authenticated_user is not None and user == authenticated_user:
                        # TODO: shouldn't the add_email get a user instead of a profile??
                        new_email = EmailAddress.objects.add_email(user=user.profile, email=request.data['new_email'])
                        new_email.set_as_primary()
                        new_email.save()  # TODO: this save might not be necessary

                        email_address_to_delete = EmailAddress.objects.get(email=user.email)

                        user.email = request.data['new_email']
                        user.save()

                        email_address_to_delete.delete()

                        return Response(status=status.HTTP_200_OK)

                    else:
                        # the authentication system was unable to verify the username and password
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'error_message': 'Password is not present'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'There is already a registered user for this email address'},
                                status=status.HTTP_409_CONFLICT)
        else:
            return Response({'error_message': 'Email is not present'}, status=status.HTTP_400_BAD_REQUEST)


class PublicNameCheckAndGet(APIView):

    permission_classes = (permissions.IsAuthenticatedForPutOrGet, permissions.CanGetUsername)

    def get_object(self, email):
        try:
            return ChUser.objects.get(email=email)
        except ChUser.DoesNotExist:
            raise Http404

    def validate_public_name(self, public_name):

        if re.match(r'^[0-9a-zA-Z_]{1,20}$', public_name):
            return
        else:
            return Response({'error_message': 'Malformed public_name'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        email = request.GET.get('email', '')
        try:
            validate_email(email)
        except Excep.ValidationError:
            return Response({'error_message': 'Email is not present or not well-formed'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = self.get_object(email)
        except ChUser.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.check_permissions(self.request)
        try:
            # If the user is requesting his/her own subscriptions we go on
            self.check_object_permissions(self.request, user.profile)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data_dict = {'public_name': user.profile.public_name}
        return Response(data=data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        if 'public_name' in request.data:
            try:
                self.validate_public_name(request.data['public_name'])
                ChUser.objects.get(profile__public_name=request.data['public_name'])
            except ChUser.DoesNotExist:
                    pass
            else:
                return Response({'error_message': 'There is already a registered user for with this public name'},
                                status=status.HTTP_409_CONFLICT)
        else:
            return Response({'error_message': 'Public_name is not present'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class ChUserList(APIView):
    """Lists all users or creates new user

    User listing is just avaliable from the browsable API, the endpoint is only exposed for a POST with a new user
    (user registration)
    """

    def check_file_extension(self, folder_plus_file_URL):
        if folder_plus_file_URL.count('.') == 1:
            extension = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
            if extension in common_settings.ALLOWED_IMAGE_EXTENSIONS:
                if folder_plus_file_URL.count('_file') == 1:
                    return
                else:
                    return Response({'error_message': 'Wrong filename'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Wrong filename'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """prueba
        """
        users = ChUser.objects.all()
        serializer = serializers.ChUserLevel2Serializer(users, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        """post prueba
        """

        if 'password' in request.data:
            if len(request.data['password']) < 8:
                return Response({'error_message': 'Password is too short'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'Password is not present'}, status=status.HTTP_400_BAD_REQUEST)

        # We check if email is valid and if there is not already a registered user with this email
        if 'email' in request.data:
            try:
                validate_email(request.data['email'])
                ChUser.objects.get(email=request.data['email'])
            except Excep.ValidationError:
                return Response({'error_message': 'Email is not well-formed'}, status=status.HTTP_400_BAD_REQUEST)
            except ChUser.DoesNotExist:
                    pass
            else:
                return Response({'error_message': 'There is already a registered user for this email address'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'Email is not present'}, status=status.HTTP_400_BAD_REQUEST)

        # Some fields are not mandatory so they might not be inside the request data
        fields_to_remove = []
        if 'city' not in request.data['profile']:
            fields_to_remove.append('city')
        if 'region' not in request.data['profile']:
            fields_to_remove.append('region')
        if 'picture' not in request.data['profile']:
            fields_to_remove.append('picture')

        serializer = serializers.ChProfileLevel2Serializer(data=request.data['profile'], fields_to_remove=fields_to_remove)

        if serializer.is_valid():

            # PROFILE PICTURE PROCESSING
            # TODO: this should be moved to a separated method

            if 'picture' in serializer.validated_data:
                pictureURL = serializer.validated_data['picture']
                if ('http://' in pictureURL) or ('https://' in pictureURL):
                    if 'amazonaws.com' in pictureURL:
                        s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                        '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                        if s3_URL_prefix in pictureURL:
                            folder_plus_file_URL = pictureURL[len(s3_URL_prefix):len(pictureURL)]
                            self.check_file_extension(folder_plus_file_URL)
                            if folder_plus_file_URL.count('/') == 1:
                                temp_folder_picture = folder_plus_file_URL[0:folder_plus_file_URL.find('/')]

                                #Temp folder has been named by the client, and the name of it must be the csrf token for the client
                                #if temp_folder_picture == django.middleware.csrf.get_token(request):
                                #    pass
                                #else:
                                #    return Response({'error_message': 'Bad S3 temp folder name'},
                                #                    status=status.HTTP_400_BAD_REQUEST)

                                file_name = folder_plus_file_URL[folder_plus_file_URL.find('/') + 1:folder_plus_file_URL.find('.')]
                                file_name_and_extension_picture = folder_plus_file_URL[folder_plus_file_URL.find('/') + 1:len(folder_plus_file_URL)]
                                file_extension_picture = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
                                folder_URL = folder_plus_file_URL[0:len(folder_plus_file_URL)-(len(file_name_and_extension_picture))]
                                # We check now if all files exist in S3
                                s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                                # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                                temp_bucket_picture = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                                s3_object_key = Key(temp_bucket_picture)
                                s3_object_key.key = folder_URL + 'file' + file_extension_picture
                                k1 = s3_object_key.exists()
                                s3_object_key.key = folder_URL + 'xlarge' + file_extension_picture
                                k2 = s3_object_key.exists()
                                s3_object_key.key = folder_URL + 'medium' + file_extension_picture
                                k3 = s3_object_key.exists()
                                s3_object_key.key = folder_URL + 'small' + file_extension_picture
                                k4 = s3_object_key.exists()

                                if not (k1 and k2 and k3 and k4):
                                    return Response({'error_message': 'Files not uploaded correctly'},
                                                    status=status.HTTP_400_BAD_REQUEST)

                                # We check everything is correct, but we won't actually move the file from the
                                # temp bucket to the final bucket in Amazon S3 without doing additional checks
                                # So we move the file at the end of the method

                            else:
                                return Response({'error_message': 'Bad S3 temp folder URL'},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'error_message': 'We only accept images hosted in ' +
                                                              common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'For now we only accept images hosted in Amazon S3'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'Content type is image but no URL is present'},
                                    status=status.HTTP_400_BAD_REQUEST)
                cache.get('')  # TODO: que pinta esto aquí??


            # AVATAR PROCESSING
            # If the an URL is present for the avatar then we have to check if we have a correlation between
            # this user, the Amazon S3 folder where the client uploaded claims to have uploaded the file and the actual
            # folder the client was allowed to upload for this user.
            # TODO: this should be moved to a separated method
            avatarURL = serializer.validated_data['avatar']
            if ('http://' in avatarURL) or ('https://' in avatarURL):
                if 'amazonaws.com' in avatarURL:
                    s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                    '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                    if s3_URL_prefix in avatarURL:
                        folder_plus_file_URL = avatarURL[len(s3_URL_prefix):len(avatarURL)]
                        self.check_file_extension(folder_plus_file_URL)
                        if folder_plus_file_URL.count('/') == 1:
                            temp_folder_avatar = folder_plus_file_URL[0:folder_plus_file_URL.find('/')]
                            file_name = folder_plus_file_URL[folder_plus_file_URL.find('/') + 1:folder_plus_file_URL.find('.')]
                            file_name_and_extension_avatar = folder_plus_file_URL[folder_plus_file_URL.find('/') + 1:len(folder_plus_file_URL)]
                            file_extension_avatar = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
                            folder_URL = folder_plus_file_URL[0:len(folder_plus_file_URL)-(len(file_name_and_extension_avatar))]
                            # We check now if all files exist in S3
                            s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                            # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                            temp_bucket_avatar = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                            s3_object_key = Key(temp_bucket_avatar)
                            s3_object_key.key = folder_URL + 'file' + file_extension_avatar
                            k5 = s3_object_key.exists()
                            s3_object_key.key = folder_URL + 'xlarge' + file_extension_avatar
                            k6 = s3_object_key.exists()
                            s3_object_key.key = folder_URL + 'medium' + file_extension_avatar
                            k7 = s3_object_key.exists()
                            s3_object_key.key = folder_URL + 'small' + file_extension_avatar
                            k8 = s3_object_key.exists()

                            if not (k5 and k6 and k7 and k8):
                                return Response({'error_message': 'Files not uploaded correctly'},
                                                status=status.HTTP_400_BAD_REQUEST)

                            # We check everything is correct, but we won't actually move the file from the
                            # temp bucket to the final bucket in Amazon S3 without doing additional checks
                            # So we move the file at the end of the method

                        else:
                            return Response({'error_message': 'Bad S3 temp folder URL'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'We only accept images hosted in ' +
                                                          common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'For now we only accept images hosted in Amazon S3'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Content type is image but no URL is present'},
                                status=status.HTTP_400_BAD_REQUEST)
            cache.get('')  # TODO: que pinta esto aquí??


            # We create the User object and the Profile object

            # Creating the new user
            email = request.data['email']
            password = request.data['password']
            # For the UserManager is the value of the username is not relevant, we pass the email instead
            username = email
            manager = ChUserManager()
            user = manager.create_user(username, email, password)

            # Creating the profile
            serializer.validated_data['user'] = user
            color = ''
            for ii in range(3):
                while True:
                    rgb = uuid4().hex[:2]
                    if 'EE' > rgb > '20':
                        break
                color = color + rgb
            serializer.validated_data['personal_color'] = '#' + color
            serializer.validated_data['private_status'] = 'I\'m new in chattyhive!'
            serializer.validated_data['public_status'] = 'I\'m new in chattyhive!'

            # TODO: esto en teoria ya salva el perfil con todos sus campos.. COMPROBAR
            profile = serializer.save()

            profile.save()

            #Creating the Email object which will handle email confimation:
            EmailAddress.objects.add_email(user=user.profile, email=email)

            # PROFILE PICTURE PROCESSING
            if 'picture' in serializer.validated_data:
                destination_bucket = common_settings.S3_PRIVATE_BUCKET
                dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
                s3_object_to_move = Key(temp_bucket_picture)

                # We need to move 3 images
                # 1 file size
                s3_object_to_move.key = temp_folder_picture + '/' + 'file' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                             + 'images' + '/' + 'file' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 2 xlarge size
                s3_object_to_move.key = temp_folder_picture + '/' + 'xlarge' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                             + 'images' + '/' + 'xlarge' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 3 medium size
                s3_object_to_move.key = temp_folder_picture + '/' + 'medium' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                             + 'images' + '/' + 'medium' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 4 small size
                s3_object_to_move.key = temp_folder_picture + '/' + 'small' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                             + 'images' + '/' + 'small' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # We also delete the folder
                folder_to_remove = temp_folder_picture + '/'
                s3_object_to_remove = Key(temp_bucket_picture)
                s3_object_to_remove.key = folder_to_remove
                s3_object_to_remove.delete()

                # We need to modify the profile with the new picture address
                profile.picture = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + \
                                  '.amazonaws.com/' + destination_bucket + '/' + 'profiles' + '/' + profile.public_name\
                                  + '/' + 'images' + '/' + 'file' + file_extension_picture

            # AVATAR PROCESSING
            destination_bucket = common_settings.S3_PUBLIC_BUCKET
            dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
            s3_object_to_move = Key(temp_bucket_avatar)

            # We need to move 3 images
            # 1 file size
            s3_object_to_move.key = temp_folder_avatar + '/' + 'file' + file_extension_avatar
            destination_object_key = Key(dest_bucket)
            destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                         + 'images' + '/' + 'file' + file_extension_avatar
            dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
            s3_object_to_move.delete()

            # 2 xlarge size
            s3_object_to_move.key = temp_folder_avatar + '/' + 'xlarge' + file_extension_avatar
            destination_object_key = Key(dest_bucket)
            destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                         + 'images' + '/' + 'xlarge' + file_extension_avatar
            dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
            s3_object_to_move.delete()

            # 3 medium size
            s3_object_to_move.key = temp_folder_avatar + '/' + 'medium' + file_extension_avatar
            destination_object_key = Key(dest_bucket)
            destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                         + 'images' + '/' + 'medium' + file_extension_avatar
            dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
            s3_object_to_move.delete()

            # 4 small size
            s3_object_to_move.key = temp_folder_avatar + '/' + 'small' + file_extension_avatar
            destination_object_key = Key(dest_bucket)
            destination_object_key.key = 'profiles' + '/' + profile.public_name + '/' \
                                         + 'images' + '/' + 'small' + file_extension_avatar
            dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
            s3_object_to_move.delete()

            # We also delete the folder
            folder_to_remove = temp_folder_avatar + '/'
            s3_object_to_remove = Key(temp_bucket_avatar)
            s3_object_to_remove.key = folder_to_remove
            s3_object_to_remove.delete()

            # We need to modify the profile with the new picture address
            profile.avatar = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + \
                              '.amazonaws.com/' + destination_bucket + '/' + 'profiles' + '/' + profile.public_name\
                              + '/' + 'images' + '/' + 'file' + file_extension_avatar

            profile.save()

            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@parser_classes((JSONParser,))
@permission_classes((permissions.IsAuthenticated,))
def password_change(request):
    if request.method == 'PUT':
        user = request.user

        if 'old_password' not in request.data:
            return Response({"error_message": "old password is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)

        if 'new_password' not in request.data:
            return Response({"error_message": "new password is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if hashers.check_password(old_password, user.password):
            new_hashed_password = hashers.make_password(new_password)
            if not hashers.is_password_usable(new_hashed_password):
                return Response({"error_message": "this new proposed password is not a valid password"}, status=status.HTTP_400_BAD_REQUEST)
            user.password = new_hashed_password
            user.save()
        else:
            return Response({"error_message": "The old password does not match the password for this user"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class ChProfileDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.CanGetProfile, permissions.CanUpdateProfile)

    def get_object(self, public_name):
        try:
            return ChProfile.objects.get(public_name=public_name)
        except ChProfile.DoesNotExist:
            raise Http404

    def check_file_extension(self, folder_plus_file_URL):

        if folder_plus_file_URL.count('.') == 1:
            extension = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
            if extension in common_settings.ALLOWED_IMAGE_EXTENSIONS:
                if folder_plus_file_URL.count('file') == 1:
                    return
                else:
                    return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)

    def remove_restricted_fields(self, user_profile, other_profile, serializer_data, profile_type):

        if profile_type == 'logged_profile':
            if user_profile == other_profile:
                pass  # nothing to be excluded!
            else:
                raise PermissionDenied
        elif profile_type == 'private':

            pass  # Code for friends implementation

        elif profile_type == 'public':
            elements_to_exclude = ['user', 'public_show_age', 'public_show_sex', 'public_show_location',
                                   'private_show_age', 'private_show_location']
            if not other_profile.public_show_age:
                elements_to_exclude.append('birth_date')
            if not other_profile.public_show_sex:
                elements_to_exclude.append('sex')
            if not other_profile.public_show_location:
                elements_to_exclude.append('country')
                elements_to_exclude.append('region')
                elements_to_exclude.append('city')
                elements_to_exclude.append('location')
            for key in serializer_data.keys():
                if key in elements_to_exclude:
                    del serializer_data[key]
        else:
            raise ValidationError

        return serializer_data

    def get(self, request, public_name, profile_type, format=None):

        other_profile = self.get_object(public_name)
        user_profile = request.user.profile

        if profile_type == "private":
            try:
                # If the user is requesting his/her own profile we go on
                self.check_object_permissions(self.request, other_profile)
            except PermissionDenied:
                # TODO: If the request is for the private profile of other user we have to check if the users are friends
                pass
            except NotAuthenticated:
                return Response(status=status.HTTP_403_FORBIDDEN)

        profile_package = request.GET.get('package', '')

        serializer = serializers.ChProfileSerializer(other_profile, type=profile_type, package=profile_package)

        allowed_data = self.remove_restricted_fields(user_profile, other_profile, serializer.data, profile_type)

        return Response(allowed_data)


    def patch(self, request, public_name, format=None):

        profile_to_update = self.get_object(public_name)
        user_profile = request.user.profile

        try:
            # If the user is requesting his/her own profile we go on
            self.check_object_permissions(self.request, profile_to_update)
        except PermissionDenied:
            return Response({'error_message': 'You can not update other profile than yours'},
                            status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        fields_to_include = list(request.data.keys())

        if 'avatar' in request.data:
            avatar = request.data['avatar']
            if ('http://' in avatar) or ('https://' in avatar):
                if 'amazonaws.com' in avatar:
                    s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                    '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                    if s3_URL_prefix in avatar:
                        folder_plus_file_URL_avatar = avatar[len(s3_URL_prefix):len(avatar)]
                        self.check_file_extension(folder_plus_file_URL_avatar)
                        if folder_plus_file_URL_avatar.count('/') == 1:
                            temp_folder_avatar = folder_plus_file_URL_avatar[0:folder_plus_file_URL_avatar.find('/')]
                            if cache.get('s3_temp_dir:' + temp_folder_avatar) == user_profile.public_name:
                                file_name_and_extension_picture = folder_plus_file_URL_avatar[folder_plus_file_URL_avatar.find('/') + 1:len(folder_plus_file_URL_avatar)]
                                file_extension_avatar = folder_plus_file_URL_avatar[folder_plus_file_URL_avatar.find('.'): len(folder_plus_file_URL_avatar)]
                                folder_URL_avatar = folder_plus_file_URL_avatar[0:len(folder_plus_file_URL_avatar)-(len(file_name_and_extension_picture))]
                                # We check now if all files exist in S3
                                s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                                # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                                temp_bucket = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                                s3_object_key = Key(temp_bucket)

                                s3_object_key.key = folder_URL_avatar + 'file' + file_extension_avatar
                                k1 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_avatar + 'xlarge' + file_extension_avatar
                                k2 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_avatar + 'medium' + file_extension_avatar
                                k3 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_avatar + 'small' + file_extension_avatar
                                k4 = s3_object_key.exists()

                                if not (k1 and k2 and k3 and k4):
                                    return Response({'error_message': 'Files not uploaded correctly'},
                                                    status=status.HTTP_400_BAD_REQUEST)

                                # We check everything is correct, but we won't actually move the file from the
                                # temp bucket to the final bucket in Amazon S3 without doing additional checks
                                # So we move the file at the end of the method


                            else:
                                return Response({'error_message': 'Upload not allowed'},
                                                status=status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({'error_message': 'Bad S3 temp folder URL'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'We only accept content hosted in ' +
                                                          common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'For now we only accept content hosted in Amazon S3'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Content type is image but no URL is present'},
                                status=status.HTTP_400_BAD_REQUEST)

        if 'picture' in request.data:
            picture = request.data['picture']
            if ('http://' in picture) or ('https://' in picture):
                if 'amazonaws.com' in picture:
                    s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                    '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                    if s3_URL_prefix in picture:
                        folder_plus_file_URL_picture = picture[len(s3_URL_prefix):len(picture)]
                        self.check_file_extension(folder_plus_file_URL_picture)
                        if folder_plus_file_URL_picture.count('/') == 1:
                            temp_folder_picture = folder_plus_file_URL_picture[0:folder_plus_file_URL_picture.find('/')]
                            if cache.get('s3_temp_dir:' + temp_folder_picture) == user_profile.public_name:
                                file_name_and_extension_picture = folder_plus_file_URL_picture[folder_plus_file_URL_picture.find('/') + 1:len(folder_plus_file_URL_picture)]
                                file_extension_picture = folder_plus_file_URL_picture[folder_plus_file_URL_picture.find('.'): len(folder_plus_file_URL_picture)]
                                folder_URL_picture = folder_plus_file_URL_picture[0:len(folder_plus_file_URL_picture)-(len(file_name_and_extension_picture))]
                                # We check now if all files exist in S3
                                s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                                # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                                temp_bucket = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                                s3_object_key = Key(temp_bucket)

                                s3_object_key.key = folder_URL_picture + 'file' + file_extension_picture
                                k1 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'xlarge' + file_extension_picture
                                k2 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'medium' + file_extension_picture
                                k3 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'small' + file_extension_picture
                                k4 = s3_object_key.exists()

                                if not (k1 and k2 and k3 and k4):
                                    return Response({'error_message': 'Files not uploaded correctly'},
                                                    status=status.HTTP_400_BAD_REQUEST)

                                # We check everything is correct, but we won't actually move the file from the
                                # temp bucket to the final bucket in Amazon S3 without doing additional checks
                                # So we move the file at the end of the method

                            else:
                                return Response({'error_message': 'Upload not allowed'},
                                                status=status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({'error_message': 'Bad S3 temp folder URL'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'We only accept content hosted in ' +
                                                          common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'For now we only accept content hosted in Amazon S3'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Content type is image but no URL is present'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ChProfileLevel2PatchSerializer(profile_to_update, data=request.data, partial=True)

        if serializer.is_valid():

            # We now move the images in case there was a change for avatar or profile picture

            if 'avatar' in request.data:
                # We need to move 4 images for the avatar
                destination_bucket = common_settings.S3_PUBLIC_BUCKET
                dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
                s3_object_to_move = Key(temp_bucket)

                # 1 file size
                s3_object_to_move.key = folder_plus_file_URL_avatar
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'file' + file_extension_avatar
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 2 xlarge size
                s3_object_to_move.key = temp_folder_avatar + '/' + 'xlarge' + file_extension_avatar
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'xlarge' + file_extension_avatar
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 3 medium size
                s3_object_to_move.key = temp_folder_avatar + '/' + 'medium' + file_extension_avatar
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'medium' + file_extension_avatar
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 4 small size
                s3_object_to_move.key = temp_folder_avatar + '/' + 'small' + file_extension_avatar
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'small' + file_extension_avatar
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # We also delete the folder
                folder_to_remove = folder_plus_file_URL_avatar[0:folder_plus_file_URL_avatar.find('/') + 1]
                s3_object_to_remove = Key(temp_bucket)
                s3_object_to_remove.key = folder_to_remove
                s3_object_to_remove.delete()

                # And we delete the entry from the cache
                cache.delete('s3_temp_dir:' + temp_folder_avatar)

                # We need to modify the profile with the new picture address
                avatar_destination_URL = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + \
                                         '.amazonaws.com/' + destination_bucket + '/' + 'profiles' + '/' + \
                                         profile_to_update.public_name + '/' + 'images' + '/' + 'file' + \
                                         file_extension_avatar

            if 'picture' in request.data:
                # We need to move 4 images for the profile picture
                destination_bucket = common_settings.S3_PRIVATE_BUCKET
                dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
                s3_object_to_move = Key(temp_bucket)

                # 1 file size
                s3_object_to_move.key = folder_plus_file_URL_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'file' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 2 xlarge size
                s3_object_to_move.key = temp_folder_picture + '/' + 'xlarge' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'xlarge' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 3 medium size
                s3_object_to_move.key = temp_folder_picture + '/' + 'medium' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'medium' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()

                # 4 small size
                s3_object_to_move.key = temp_folder_picture + '/' + 'small' + file_extension_picture
                destination_object_key = Key(dest_bucket)
                destination_object_key.key = 'profiles' + '/' + user_profile.public_name + '/' \
                                             + 'images' + '/' + 'small' + file_extension_picture
                dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                s3_object_to_move.delete()


                # We also delete the folder
                folder_to_remove = folder_plus_file_URL_picture[0:folder_plus_file_URL_picture.find('/') + 1]
                s3_object_to_remove = Key(temp_bucket)
                s3_object_to_remove.key = folder_to_remove
                s3_object_to_remove.delete()

                # And we delete the entry from the cache
                cache.delete('s3_temp_dir:' + temp_folder_picture)

                # We need to modify the profile with the new picture address
                picture_destination_URL = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + \
                                  '.amazonaws.com/' + destination_bucket + '/' + 'profiles' + '/' + profile_to_update.public_name\
                                  + '/' + 'images' + '/' + 'file' + file_extension_picture

            # We finally update the profile with the data from the serializer
            profile_to_update = serializer.save()
            if 'picture' in request.data:
                profile_to_update.picture = picture_destination_URL
            if 'avatar' in request.data:
                profile_to_update.avatar = avatar_destination_URL
            profile_to_update.save()

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChUserDetail(APIView):
    """Show user detail, updates user detail or deletes specific user

    User detail is just available from the browsable API
    (user registration)
    """

    permission_classes = (permissions.IsAuthenticated, permissions.IsAuthenticatedOrReadOnly)

    def get_object(self, username):
        try:
            return ChUser.objects.get(username=username)
        except ChUser.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = serializers.ChUserLevel2Serializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        serializer = serializers.ChUserLevel2Serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = self.get_object(username)
        # TODO: aquí donde normalmente se llamaría al método user.delete() yo llamo a delete_account() que entiendo es
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
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        hive_subscriptions = profile.hive_subscriptions

        serializer = serializers.ChHiveSubscriptionListLevel3Serializer(hive_subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, public_name, format=None):

        profile = self.get_object(public_name)
        try:
            # If the user is requesting a join with his own profile then we go on
            self.check_object_permissions(self.request, profile)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        hive_slug = request.data.get('hive_slug', '')

        if hive_slug == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # We get the hive for this hive_slug
        try:
            hive = ChHive.objects.get(slug=hive_slug, deleted=False)
        except ChHive.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hive.join(profile)
        except IntegrityError:
            return Response({'error_message': 'The user was already subscribed to the hive'},
                            status=status.HTTP_409_CONFLICT)
        except UnauthorizedException:
            return Response({'error_message': 'The user is expelled from the hive'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Because I don't want Django Rest Framework to treat it as a serializer in this case, I cast it to a dict
        hive_info = dict(serializers.ChHiveSerializer(hive).data)

        return Response(hive_info, status=status.HTTP_200_OK)


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
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        chat_subscriptions = profile.chat_subscriptions
        serializer = serializers.ChChatSubscriptionListLevel4Serializer(chat_subscriptions, many=True)
        return Response(serializer.data)


class ChProfileHiveDetail(APIView):
    """API method: Hive list

    """
    permission_classes = (permissions.IsAuthenticated, permissions.CanGetHiveList)

    def get_object(self, public_name):
        try:
            return ChProfile.objects.select_related().get(public_name=public_name)
        except ChProfile.DoesNotExist:
            raise Http404

    def delete(self, request, public_name, hive_slug, format=None):

        profile = self.get_object(public_name)
        try:
            # If the user is requesting a join with his own profile then we go on
            self.check_object_permissions(self.request, profile)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if hive_slug == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # We get the hive for this hive_slug
        try:
            hive = ChHive.objects.get(slug=hive_slug, deleted=False)
        except ChHive.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hive.leave(profile)
        except IntegrityError:
            return Response({'error_message': 'User have not joined the hive'},
                            status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_200_OK)


# ============================================================ #
#                       Hives & Chats                          #
# ============================================================ #

class ChHiveList(APIView):  # AKA Explore
    """Lists hives in Explore or creates new hive

    User listing is just avaliable from the browsable API, the endpoint is only exposed for a POST with a new user
    (user registration)
    """

    permission_classes = (permissions.IsAuthenticated,)

    def check_file_extension(self, folder_plus_file_URL):

        if folder_plus_file_URL.count('.') == 1:
            extension = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
            if extension in common_settings.ALLOWED_IMAGE_EXTENSIONS:
                if folder_plus_file_URL.count('file') == 1:
                    return
                else:
                    return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'Wrong filename'},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, list_order='', category_code='', format=None):
        """prueba
        """
        location = {}

        # Info retrieval
        profile = request.user.profile

        tags = request.query_params.getlist('tags')

        include_subscribed_string = request.query_params.get('include_subscribed', 'False')
        include_subscribed = False

        if include_subscribed_string == 'True':
            include_subscribed = True

        search_string =request.query_params.get('search_string', '')

        coordinates = request.query_params.get('coordinates', '')
        if coordinates != '':
            location['coordinates'] = coordinates

        else:  # If we get coordinates we discard anything else
            country = request.query_params.get('country', '')
            if country != '':
                location['country'] = country

            region = request.query_params.get('region', '')
            if region != '':
                location['region'] = region

            city = request.query_params.get('city', '')
            if city != '':
                location['city'] = region

            # We check if the params are coherent
            if 'city' in location:
                if 'region' not in location:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            if 'region' in location:
                if 'country' not in location:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        if list_order and category_code:  # Can not be both present at the same time!
            return Response(status=status.HTTP_400_BAD_REQUEST)

        elif list_order or category_code:
            if search_string:
                return Response({'error_message': 'if search_string is present no other params should be'},
                                status=status.HTTP_400_BAD_REQUEST)
            if category_code:
                try:
                    category_id = ChCategory.objects.get(code=category_code)
                except ChCategory.DoesNotExist:
                    return Response({'error_message': 'Category not found by this code'},
                                    status=status.HTTP_404_NOT_FOUND)
                hives = ChHive.get_hives_by_category(profile=profile, category=category_id, location=location,
                                                     tags=tags, include_subscribed=include_subscribed)
            elif list_order:
                if list_order == 'recommended':
                    hives = ChHive.get_hives_by_priority(profile=profile, tags=tags,
                                                         include_subscribed=include_subscribed)
                elif list_order == 'near':
                    hives = ChHive.get_hives_by_proximity_or_location(profile=profile, location=location,
                                                                      tags=tags, include_subscribed=include_subscribed)
                elif list_order == 'recent':
                    hives = ChHive.get_hives_by_age(profile=profile, tags=tags, include_subscribed=include_subscribed)
                elif list_order == 'communities':
                    hives = ChHive.get_communities(profile=profile, location=location,
                                                   tags=tags, include_subscribed=include_subscribed)
                elif list_order == 'top':
                    hives = ChHive.get_hives_by_subscriptions_number(profile=profile,
                                                                     tags=tags, include_subscribed=include_subscribed)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        else:  # no parameters, we just give back all hives or perform the search if search_string present
            if search_string:
                hives = ChHive.get_hives_containing(profile=profile, search_string=search_string,
                                                    include_subscribed=include_subscribed)
            else:
                hives = ChHive.get_hives_by_age(profile=profile, tags=tags, include_subscribed=include_subscribed)

        serializer = serializers.ChHiveLevel1Serializer(hives, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """post prueba
        """

        user = request.user
        profile = ChProfile.objects.get(user=user)
        fields_to_remove = []

        if 'visibility_country' not in request.data:
            fields_to_remove.append('visibility_country')

        if 'tags' in request.data:
            if len(request.data['tags']) > 5:
                return Response({'error_message': 'a maximum of 5 tags are allowed'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate tags
            tagsList = request.data['tags']

            pattern = re.compile("^\w{1,32}$")
            for tag in tagsList:
                if not pattern.match(tag):
                    return Response({'error_message': 'validation error with tags'},
                                     status=status.HTTP_400_BAD_REQUEST)

        if 'picture' in request.data:
            picture = request.data['picture']
            if ('http://' in picture) or ('https://' in picture):
                if 'amazonaws.com' in picture:
                    s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                    '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                    if s3_URL_prefix in picture:
                        folder_plus_file_URL_picture = picture[len(s3_URL_prefix):len(picture)]
                        self.check_file_extension(folder_plus_file_URL_picture)
                        if folder_plus_file_URL_picture.count('/') == 1:
                            temp_folder_picture = folder_plus_file_URL_picture[0:folder_plus_file_URL_picture.find('/')]
                            if cache.get('s3_temp_dir:' + temp_folder_picture) == profile.public_name:
                                file_name_and_extension_picture = folder_plus_file_URL_picture[folder_plus_file_URL_picture.find('/') + 1:len(folder_plus_file_URL_picture)]
                                file_extension_picture = folder_plus_file_URL_picture[folder_plus_file_URL_picture.find('.'): len(folder_plus_file_URL_picture)]
                                folder_URL_picture = folder_plus_file_URL_picture[0:len(folder_plus_file_URL_picture)-(len(file_name_and_extension_picture))]
                                # We check now if all files exist in S3
                                s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                                # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                                temp_bucket = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                                s3_object_key = Key(temp_bucket)

                                s3_object_key.key = folder_URL_picture + 'file' + file_extension_picture
                                k1 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'large' + file_extension_picture
                                k2 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'medium' + file_extension_picture
                                k3 = s3_object_key.exists()
                                s3_object_key.key = folder_URL_picture + 'small' + file_extension_picture
                                k4 = s3_object_key.exists()

                                if not (k1 and k2 and k3 and k4):
                                    return Response({'error_message': 'Files not uploaded correctly'},
                                                    status=status.HTTP_400_BAD_REQUEST)

                                # We check everything is correct, but we won't actually move the file from the
                                # temp bucket to the final bucket in Amazon S3 without doing additional checks
                                # So we move the file at the end of the method

                            else:
                                return Response({'error_message': 'Upload not allowed'},
                                                status=status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({'error_message': 'Bad S3 temp folder URL'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'We only accept content hosted in ' +
                                                          common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'For now we only accept content hosted in Amazon S3'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Content type is image but no URL is present'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            fields_to_remove.append('picture')

        serializer = serializers.ChHiveCreationSerializer(data=request.data, fields_to_remove=fields_to_remove)

        if serializer.is_valid():
            with transaction.atomic():

                hive = ChHive(name=serializer.validated_data['name'],
                              description=serializer.validated_data['description'],
                              category=serializer.validated_data['category'],
                              type=serializer.validated_data['type'],
                              creation_date=timezone.now(),
                              priority=50,
                              rules=GuidelinesModel.objects.get(name="Base guidelines")
                              )

                hive.creator = profile

                hive.slug = slugify(serializer.validated_data['name'], translate=None, to_lower=True, separator='-',
                                    capitalize=False, max_length=250)

                if 'visibility_country' in request.data:
                    hive.visibility_country = serializer.validated_data['visibility_country']

                if 'picture' in request.data:
                    hive.picture = serializer.validated_data['picture']

                try:
                    with transaction.atomic():
                        ChHive.objects.get(slug=hive.slug)
                        return Response({'error_message': 'There is already a Hive with this or very similar name'},
                                        status=status.HTTP_409_CONFLICT)
                except ChHive.DoesNotExist:
                    # hive.slug = replace_unicode(hive_name)
                    hive.save()

                hive.languages = serializer.validated_data['_languages']

                if 'tags' in request.data:
                    hive.set_tags(tagsList)
                    hive.save()

                # Adding languages
                # hive.languages = formHive.cleaned_data['_languages']
                # hive.save()

                if serializer.validated_data['type'] == 'Hive':
                    # Creating public chat of hive, step 1: ChChat object
                    chat = ChChat()
                    chat.hive = hive
                    chat.type = 'public'
                    chat.chat_id = ChChat.get_chat_id()
                    chat.slug = chat.chat_id + '-' + hive.slug
                    chat.save()

                    # Creating public chat of hive, step 2: ChPublicChat object
                    public_chat = ChPublicChat(chat=chat, hive=hive)
                    public_chat.slug = slugify(serializer.validated_data['name'], translate=None, to_lower=True,
                                               separator='-', capitalize=False, max_length=250)
                    public_chat.save()

                elif serializer.validated_data['type'] == 'Community':
                    # Creating community from hive
                    community = ChCommunity(hive=hive, owner=profile)
                    community.approved = True  # TODO: This is temporal solution.
                    community.save()

                    # Creating public chat of hive
                    community.new_public_chat(name=hive.name, public_chat_slug_ending=hive.slug, description=hive.description)

                if 'picture' in request.data:

                    # We need to move 4 images for the profile picture
                    destination_bucket = common_settings.S3_PUBLIC_BUCKET
                    dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
                    s3_object_to_move = Key(temp_bucket)

                    # 1 file size
                    s3_object_to_move.key = folder_plus_file_URL_picture
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'hives' + '/' + hive.slug + '/' \
                                                 + 'images' + '/' + 'file' + file_extension_picture
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # 2 large size
                    s3_object_to_move.key = temp_folder_picture + '/' + 'large' + file_extension_picture
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'hives' + '/' + hive.slug + '/' \
                                                 + 'images' + '/' + 'large' + file_extension_picture
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # 3 medium size
                    s3_object_to_move.key = temp_folder_picture + '/' + 'medium' + file_extension_picture
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'hives' + '/' + hive.slug + '/' \
                                                 + 'images' + '/' + 'medium' + file_extension_picture
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # 4 small size
                    s3_object_to_move.key = temp_folder_picture + '/' + 'small' + file_extension_picture
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'hives' + '/' + hive.slug + '/' \
                                                 + 'images' + '/' + 'small' + file_extension_picture
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # We also delete the folder
                    folder_to_remove = folder_plus_file_URL_picture[0:folder_plus_file_URL_picture.find('/') + 1]
                    s3_object_to_remove = Key(temp_bucket)
                    s3_object_to_remove.key = folder_to_remove
                    s3_object_to_remove.delete()

                    # And we delete the entry from the cache
                    cache.delete('s3_temp_dir:' + temp_folder_picture)

                    # We need to modify the profile with the new picture address
                    picture_destination_URL = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + \
                                      '.amazonaws.com/' + destination_bucket + '/' + 'hives' + '/' + hive.slug \
                                      + '/' + 'images' + '/' + 'file' + file_extension_picture

                    hive.picture = picture_destination_URL
                    hive.save()

                # Creating subscription
                hive_subscription = ChHiveSubscription(hive=hive, profile=profile)
                hive_subscription.save()

                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        fields_to_remove = ()
        serializer = serializers.ChHiveSerializer(hive, fields_to_remove=fields_to_remove)

        return Response(serializer.data)


class ChHiveUsersList(APIView):
    """API method: GET hive info

    """

    permission_classes = (permissions.IsAuthenticated, permissions.CanGetHiveUsers)

    def get_object(self, hive_slug):
        try:
            return ChHive.objects.get(slug=hive_slug)
        except ChHive.DoesNotExist:
            raise Http404

    def get(self, request, hive_slug, list_order, format=None):

        # Info retrieval
        hive = self.get_object(hive_slug)
        profile = request.user.profile

        try:
            # If the user is requesting users for a hive he/she is subscribed, then we go on...
            self.check_object_permissions(self.request, hive)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if list_order == 'recommended':
            profiles = hive.get_users_recommended(profile)
        elif list_order == 'near':
            # TODO: This could be much more improved, using the latitude and longitude data on the database,
            # but using cities, regions and countries is not bad solution at all
            profiles = hive.get_users_near(profile)
        elif list_order == 'recent':
            profiles = hive.get_users_recently_online(profile)
        elif list_order == 'new':
            profiles = hive.get_users_recently_join(profile)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ChProfileSerializer(profiles, many=True, type='public', package='basic')

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

    def check_file_extension(self, folder_plus_file_URL, content_type):

        if content_type == 'image':
            if folder_plus_file_URL.count('.') == 1:
                extension = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
                if extension in common_settings.ALLOWED_IMAGE_EXTENSIONS:
                    if folder_plus_file_URL.count('file') == 1:
                        return
                    else:
                        return Response({'error_message': 'Wrong filename'},
                                status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'Wrong filename'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Wrong filename'},
                                status=status.HTTP_400_BAD_REQUEST)
        return

    def get(self, request, chat_id, format=None):
        chat = self.get_chat(chat_id)
        try:
            self.check_object_permissions(self.request, chat)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
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
        if 'dev_id' not in request.data:
            fields_to_remove.append('dev_id')

        serializer = serializers.SendMessageSerializer(data=request.data, fields_to_remove=fields_to_remove)

        if serializer.is_valid():
            # info retrieval
            new_chat = request.data.get("new_chat", "False")
            profile = request.user.profile
            socket_id = serializer.validated_data['socket_id']
            content_type = serializer.validated_data['content_type']
            msg_content = serializer.validated_data['content']

            # If the message is an image then we have to check if we have a correlation between this user,
            # the Amazon S3 folder where the client uploaded claims to have uploaded the file and the actual
            # folder the client was allowed to upload for this user.
            # TODO: this should be moved to a separated method

            if content_type == 'image' or content_type == 'video' or content_type == 'audio' or\
                            content_type == 'animation' or content_type == 'file':
                if ('http://' in msg_content) or ('https://' in msg_content):
                    if 'amazonaws.com' in msg_content:
                        s3_URL_prefix = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION +\
                                        '.amazonaws.com/' + common_settings.S3_TEMP_BUCKET + '/'
                        if s3_URL_prefix in msg_content:
                            folder_plus_file_URL = msg_content[len(s3_URL_prefix):len(msg_content)]
                            self.check_file_extension(folder_plus_file_URL, content_type)
                            if folder_plus_file_URL.count('/') == 1:
                                temp_folder = folder_plus_file_URL[0:folder_plus_file_URL.find('/')]
                                if cache.get('s3_temp_dir:' + temp_folder) == profile.public_name:
                                    file_name_and_extension = folder_plus_file_URL[folder_plus_file_URL.find('/') + 1:len(folder_plus_file_URL)]
                                    file_extension = folder_plus_file_URL[folder_plus_file_URL.find('.'): len(folder_plus_file_URL)]
                                    folder_URL = folder_plus_file_URL[0:len(folder_plus_file_URL)-(len(file_name_and_extension))]
                                    # We check now if all files exist in S3
                                    s3_connection = S3Connection(common_settings.AWS_ACCESS_KEY_ID, common_settings.AWS_SECRET_ACCESS_KEY)
                                    # With validate=False we save an AWS request, we do this because we are 100% sure the bucket exists
                                    temp_bucket = s3_connection.get_bucket(common_settings.S3_TEMP_BUCKET, validate=False)
                                    s3_object_key = Key(temp_bucket)

                                    if content_type == 'image':

                                        s3_object_key.key = folder_URL + 'file' + file_extension
                                        k1 = s3_object_key.exists()
                                        s3_object_key.key = folder_URL + 'xlarge' + file_extension
                                        k2 = s3_object_key.exists()
                                        s3_object_key.key = folder_URL + 'medium' + file_extension
                                        k3 = s3_object_key.exists()

                                        if not (k1 and k2 and k3):
                                            return Response({'error_message': 'Files not uploaded correctly'},
                                                            status=status.HTTP_400_BAD_REQUEST)

                                        # We check everything is correct, but we won't actually move the file from the
                                        # temp bucket to the final bucket in Amazon S3 without doing additional checks
                                        # So we move the file at the end of the method

                                    else:  # for any other content-type
                                        s3_object_key.key = folder_URL + 'file' + file_extension
                                        k1 = s3_object_key.exists()

                                        if not k1:
                                            return Response({'error_message': 'Files not uploaded correctly'},
                                                            status=status.HTTP_403_FORBIDDEN)
                                else:
                                    return Response({'error_message': 'Upload not allowed'},
                                                    status=status.HTTP_403_FORBIDDEN)
                            else:
                                return Response({'error_message': 'Bad S3 temp folder URL'},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'error_message': 'We only accept content hosted in ' +
                                                              common_settings.S3_TEMP_BUCKET + 'and in a secure connection'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error_message': 'For now we only accept content hosted in Amazon S3'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'Content type is image but no URL is present'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # cache.get('')  # TODO: que pinta esto aquí??

            elif content_type == 'text':
                pass
            else:
                return Response({'error_message': 'Wrong content_type'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Initialization of the message to be sent
            message_data = {'profile': profile}

            # If the client has sent a dev_id we update the last_activity field of the device to the date
            if 'dev_id' in serializer.validated_data:
                try:
                    device = Device.objects.get(dev_id=serializer.validated_data['dev_id'], active=True)
                    device.last_activity = timezone.now()
                    device.save()
                except Device.DoesNotExist:
                    return Response({'error_message': 'No device found for this dev_id'}, status=status.HTTP_404_NOT_FOUND)

            if new_chat.lower() == 'true':
                # In this case the client should be actually sending us a temp_id that is the chat slug
                # We extract the relevant info from it:
                chat_slug = chat_id
                if chat_slug.find('-') == -1:  # new_chat == True and a chat_id without a slug format shouldn't happen
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    if chat_slug.find('+') != -1:  # This is a chat between friends
                        pass  # TODO
                    elif chat_slug.find('--') != -1:  # This is a chat between hivemates inside a hive
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
                            return Response(status=status.HTTP_403_FORBIDDEN)

                        # We search for any other ChChat object with the same ending. Just in case the other profile was also
                        # starting a new chat (he/she would have a different temporal chat_id assigned).
                        try:
                            with transaction.atomic():
                                chat = ChChat.objects.get(hive=hive, slug__endswith=slug_ends_with)
                        except ChChat.DoesNotExist:
                            chat = ChChat(chat_id=chat_id, slug=chat_slug, type='mate_private', hive=hive)
                            chat.save()
                    else:  # This could be a public chat
                        return Response({"error_message": "Wrong slug, or public chat and new=True incompatible"},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:  # new_chat == False
                try:
                    with transaction.atomic():
                        # TODO: Additional checks here if chat is between friends (has the user been blocked by the target user?)
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
                                return Response(status=status.HTTP_403_FORBIDDEN)
                        else:  # This is a public chat
                            hive = chat.hive
                            try:
                                with transaction.atomic():
                                    hive_subscription = \
                                        ChHiveSubscription.objects.select_related().get(hive=hive,
                                                                                        profile=profile,
                                                                                        subscription_state='active')
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
                        if other_chat_subscription.subscription_state == 'deleted':
                            other_chat_subscription.subscription_state = 'active'
                            other_chat_subscription.save()
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

            if content_type == 'image' or content_type == 'video' or content_type == 'audio' or\
                            content_type == 'animation' or content_type == 'file':
                # We move the files from temp bucket to destination bucket
                if chat.type == 'public':
                    destination_bucket = common_settings.S3_PUBLIC_BUCKET
                else:
                    destination_bucket = common_settings.S3_PRIVATE_BUCKET
                dest_bucket = s3_connection.get_bucket(destination_bucket, validate=False)
                s3_object_to_move = Key(temp_bucket)

                if content_type == 'image':

                    # We are taking the last 6 digits of the chat count for this message
                    file_name_unique_id = str(chat.count + 1)
                    new_file_name = 'IMG_' + timezone.now().strftime("%Y%m%d_%H%M%S") + '_' + file_name_unique_id[-6:]

                    # We need to move 3 images
                    # 1 file size
                    s3_object_to_move.key = folder_plus_file_URL
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'chats' + '/' + chat.chat_id + '/' \
                                                 + 'images' + '/' + 'file' + '/' + new_file_name + file_extension
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # 2 xlarge size
                    s3_object_to_move.key = temp_folder + '/' + 'xlarge' + file_extension
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'chats' + '/' + chat.chat_id + '/' \
                                                 + 'images' + '/' + 'xlarge' + '/' + new_file_name + file_extension
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # 3 medium size
                    s3_object_to_move.key = temp_folder + '/' + 'medium' + file_extension
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'chats' + '/' + chat.chat_id + '/' \
                                                 + 'images' + '/' + 'medium' + '/' + new_file_name + file_extension
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

                    # We also delete the folder
                    folder_to_remove = folder_plus_file_URL[0:folder_plus_file_URL.find('/') + 1]
                    s3_object_to_remove = Key(temp_bucket)
                    s3_object_to_remove.key = folder_to_remove
                    s3_object_to_remove.delete()

                    # And we delete the entry from the cache
                    cache.delete('s3_temp_dir:' + temp_folder)

                    # We need to modify the message content with the new URL
                    msg_content = 'https://' + common_settings.S3_PREFIX + '-' + common_settings.S3_REGION + '.amazonaws.com/' + destination_bucket + '/' + 'chats' + '/' + chat.chat_id + '/' + 'images' + \
                                  '/' + 'file' + '/' + new_file_name + file_extension

                else:

                    # We are taking the last 6 digits of the chat count for this message
                    file_name_unique_id = str(chat.count + 1)

                    if content_type == 'video':
                        new_file_name = 'VID_' + timezone.now().strftime("%Y%m%d_%H%M%S") + '_' + file_name_unique_id[-6:]

                    if content_type == 'audio':
                        new_file_name = 'AUD_' + timezone.now().strftime("%Y%m%d_%H%M%S") + '_' + file_name_unique_id[-6:]

                    if content_type == 'animation':
                        new_file_name = 'ANI_' + timezone.now().strftime("%Y%m%d_%H%M%S") + '_' + file_name_unique_id[-6:]

                    if content_type == 'file':
                        new_file_name = 'FILE_' + timezone.now().strftime("%Y%m%d_%H%M%S") + '_' + file_name_unique_id[-6:]

                    # We need to move the file to the destination bucket
                    s3_object_to_move.key = folder_plus_file_URL
                    destination_object_key = Key(dest_bucket)
                    destination_object_key.key = 'chats' + '/' + chat.chat_id + '/' \
                                                 + content_type + 's' + '/' + 'file' + '/' + new_file_name + file_extension
                    dest_bucket.copy_key(destination_object_key, common_settings.S3_TEMP_BUCKET, s3_object_to_move.key)
                    s3_object_to_move.delete()

            message = chat.new_message(profile=profile,
                                       content_type=content_type,
                                       content=msg_content,)

            chat.save()
            chat_subscription_profile.profile_last_activity = timezone.now()
            chat_subscription_profile.save()
            if chat.type == 'public':
                hive_subscription.profile_last_activity = timezone.now()
                hive_subscription.save()
            message_data['socket_id'] = socket_id

            if new_chat.lower() == 'true':
                message_chat_id = chat_slug
            else:
                message_chat_id = chat_id

            message_data['json_message'] = json.dumps({"chat_id": message_chat_id,
                                                       "message_id": message.id,
                                                       "public_name": profile.public_name,
                                                       "content": msg_content,
                                                       "server_time": message.created.astimezone()},
                                                      cls=DjangoJSONEncoder)

            data_dict = {'message_id': message.id, 'server_timestamp': message.created}

            chat.send_message(message_data)

            if new_chat.lower() == 'true':
                data_dict['chat_id'] = chat_id
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
                ChHiveSubscription.objects.get(profile=profile, hive=hive, subscription_state='active')
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


@api_view(['GET'])
@parser_classes((JSONParser,))
def get_countries(request, format=None):
    """Returns a list of country codes
    """
    if request.method == 'GET':
        country_codes = []
        for country in Country.objects.all():
            country_codes.append(country.code2)

        return Response(data=country_codes, status=status.HTTP_200_OK)


@api_view(['GET'])
@parser_classes((JSONParser,))
def get_regions(request, country_code, format=None):
    """Returns a list of country codes
    """
    if request.method == 'GET':
        country = Country.objects.get(code2=country_code)
        region_names = []

        for region in Region.objects.filter(country=country):
            region_names.append(region.name)

        return Response(data=region_names, status=status.HTTP_200_OK)


@api_view(['GET'])
@parser_classes((JSONParser,))
def get_cities(request, country_code, region_name, format=None):
    """Returns a list of country codes
    """
    if request.method == 'GET':
        country = Country.objects.get(code2=country_code)
        region = Region.objects.get(country=country, name=region_name)
        city_names = []

        for city in City.objects.filter(country=country, region=region):
            city_names.append(city.name)

        return Response(data=city_names, status=status.HTTP_200_OK)