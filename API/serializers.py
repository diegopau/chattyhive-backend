from rest_framework import serializers, status
from rest_framework.response import Response
from core.models import *
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, ValidationError
import re


# ============================================================ #
#                      Support Classes                         #
# ============================================================ #

class URLParamsError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


# ================================================================================== #
#                     Session & 3rd-party services serializers                       #
# ================================================================================== #

class LoginCredentialsSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """
    email = serializers.EmailField()
    public_name = serializers.CharField(max_length=20, validators=[RegexValidator(r'^[0-9a-zA-Z_]+$', 'Only alphanumeric characters and "_" are allowed.')])
    password = serializers.CharField(write_only=True)
    dev_os = serializers.CharField(max_length=20)
    dev_type = serializers.CharField(max_length=20)
    dev_id = serializers.CharField(max_length=50)

    # In the init we will check which fields the view is telling the serializer to consider (this is because the
    # serializer can't know which of the files email or public_name will be present
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(LoginCredentialsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, data):
        DEV_OS_CHOICES = ('android', 'ios', 'wp', 'browser', 'windows', 'linux', 'mac')
        DEV_TYPE_CHOICES = ('smartphone', '6-8tablet', 'big_tablet', 'laptop', 'desktop', 'big_screen_desktop', 'tv')

        if 'email' in data:
            # We set to an empty string the param that is not inside the request body
            try:
                user = ChUser.objects.get(email=data['email'])
                # For security reasons we return a 401 instead of a 404 (we don't want to give clues of who is or who
                # is not registered in the service
            except ChUser.DoesNotExist:
                raise ValidationError("Unauthorized", code="401")
            data['username'] = user.username
        elif 'public_name' in data:
            try:
                profile = ChProfile.objects.select_related().get(public_name=data['public_name'])
            except ChProfile.DoesNotExist:
                raise ValidationError("The ChUser object, obtained from the profile, does not exist", code="401")
            data['username'] = profile.username
        else:
            raise serializers.ValidationError("No email or public_name specified")

        if 'dev_os' in data:
            if data['dev_os'] not in DEV_OS_CHOICES:
                raise ValidationError("Wrong dev_os", code="400")
        if 'dev_type' in data:
            if data['dev_type'] not in DEV_TYPE_CHOICES:
                raise ValidationError("Wrong dev_type", code="400")

        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']


class AsyncServices(serializers.Serializer):

    name = serializers.CharField(max_length=20)
    app = serializers.CharField(max_length=255)
    reg_id = serializers.CharField(max_length=255)

    def validate(self, data):
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        name = self.validated_data['name']
        app = self.validated_data['app']
        reg_id = self.validated_data['reg_id']


class SetAsyncServices(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """

    services = AsyncServices(many=True)

    def validate(self, data):
        for service in data['services']:
            if service['name'] == 'gcm':
                if service["app"] == "":
                    raise ValidationError("app field for gcm can not be empty", code="400")
                elif service["app"] not in settings.ALLOWED_GCM_APP_IDS:
                    raise ValidationError("app id for gcm not allowed", code="400")
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        services = self.validated_data['services']


class AsyncAuthSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """

    service = serializers.CharField(max_length=30)
    channel_name = serializers.CharField(max_length=41)
    socket_id = serializers.CharField(max_length=255)

    def validate(self, data):
        if data['service'] == 'pusher':
            # We set to an empty string the param that is not inside the request body
            if data['channel_name'].starts_with('presence-'):
                chat_id = data['channel_name'][9:len(data['channel_name'])]
                try:
                    ChChat.objects.get(chat_id=chat_id)
                except ChUser.DoesNotExist:
                    raise ValidationError("The chat belonging to that channel does not exist.", code="404")
            else:
                raise ValidationError("The channel_name does not have the correct format.", code="400")
        else:
            raise ValidationError("Only 'pusher' service is accepted by now.", code="400")
        if data['socket_id'] == '':
            raise ValidationError("Socket_id can not be empty", code="400")
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        service = self.validated_data['service']
        channel_name = self.validated_data['channel_name']
        socket_id = self.validated_data['socket_id']


# ============================================================= #
#                       Other serializers                       #
# ============================================================= #

class SendMessageSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """

    content_type = serializers.CharField(max_length=20)
    client_timestamp = serializers.CharField(max_length=30)
    content = serializers.CharField(max_length=2048)
    new_chat = serializers.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass

        fields_to_remove = kwargs.pop('fields_to_remove', None)

        # Instantiate the superclass normally
        super(SendMessageSerializer, self).__init__(*args, **kwargs)

        if fields_to_remove is not None:
            # Drop fields that are specified in the `fields` argument.
            for field_name in fields_to_remove:
                self.fields.pop(field_name)

    def validate(self, data):

        CONTENTS = ('text', 'image', 'video', 'audio', 'animation', 'url', 'file', 'invitation')
        BOOLEANS = ('true', 'false', 'True', 'False')

        if data['content_type'] not in CONTENTS:
            raise ValidationError("Wrong content_type", code="400")
        if 'new_chat' in data:
            if data['new_chat'] not in BOOLEANS:
                raise ValidationError("Wrong new_chat value", code="400")
        if data['content'] == '':
            raise ValidationError("The message content is empty", code="400")
        if data['client_timestamp'] == '':
            raise ValidationError("No client timestamp specified", code="400")
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        content_type = self.validated_data['content_type']
        client_timestamp = self.validated_data['client_timestamp']
        content = self.validated_data['content']
        new_chat = self.validadted_data['new_chat']


# =================================================================== #
#                     Simple Model Serializers                        #
# =================================================================== #
class ChCommunityLevel1Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET hive info,
       Used by the following serializers:

    """
    admins = serializers.SlugRelatedField(slug_field='public_name', many=True, read_only=True)
    owner = serializers.SlugRelatedField(slug_field='public_name', read_only=True)

    class Meta:
        model = ChCommunity
        fields = ('admins', 'owner')


class ChPublicChatLevel1Serializer(serializers.ModelSerializer):
    chat = serializers.SlugRelatedField(read_only=True, slug_field='chat_id', allow_null=True)

    class Meta:
        model = ChPublicChat
        fields = ('chat', )


class ChCommunityPublicChatLevel1Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET chat info,

    """

    moderators = serializers.SlugRelatedField(many=True, slug_field='public_name', read_only=True)

    class Meta:
        model = ChCommunityPublicChat
        fields = ('name', 'description', 'moderators', 'rules', 'picture')


class ChCommunityPublicChatListLevel1Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET hive list,

    """
    chat = serializers.SlugRelatedField(read_only=True, slug_field='chat_id', allow_null=True)

    class Meta:
        model = ChCommunityPublicChat
        fields = ('chat', )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ('language', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('tag', )


# Serializers define the API representation.
class ChUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChUser
        fields = ('date_joined', 'email', 'is_active', 'is_authenticated', 'is_staff', 'objects', 'related_device',
                  'username')


class ChChatLevel0Serializer(serializers.ModelSerializer):
    class Meta:
        model = ChChat
        fields = ('count', 'type', 'hive', 'chat_id', 'created')


class ChMessageLevel1Serializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(read_only=True, slug_field='public_name')

    class Meta:
        model = ChMessage
        fields = ('content_type', 'received', 'content', 'profile')


# ============================================================ #
#                       Users & Profiles                       #
# ============================================================ #

# This support class will allow the other related ModelSerializers to use only the needed fields (depending on the
# url path params and query params
# class SelectProfileFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         profile_type = kwargs.pop('type', None)
#         profile_package = kwargs.pop('package', None)
#
#         # Instantiate the superclass normally
#         super(SelectProfileFieldsModelSerializer, self).__init__(*args, **kwargs)
#
#         # In the related ModelSerializers we will set all possible fields, with this code we will dynamically
#         # drop some of these fields depending on the url path params and the query params of the client request
#         existing_fields = set(self.fiedls.keys())  # This will be all the fields that are set in the ModelSerializer
#
#         if profile_type is not None:
#             if profile_type == 'public':
#                 if profile_package is not None:
#                     if profile_package == 'basic'
#                         allowed_fields = set("username", "public_name", )
#                     elif profile_package == 'info'
#
#                     elif profile_package == 'hives'
#
#                     elif profile_package == 'complete'
#
#                     else:
#                         raise URLParamsError("The profile_package value doesn't match any API defined value", errors={})
#                 else:
#                     raise URLParamsError("No profile package specified", errors={})
#             elif profile_type == 'private':
#                 if profile_package is not None:
#                     if profile_package == 'basic'
#
#                     elif profile_package == 'info'
#
#                     elif profile_package == 'hives'
#
#                     elif profile_package == 'complete'
#
#                     else:
#                         raise URLParamsError("The profile_package value doesn't match any API defined value", errors={})
#                 else:
#                     raise URLParamsError("No profile package specified", errors={})
#             else:
#                 allowed_fields = set("", "")
#
#         if allowed_fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(allowed_fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#
#
# class ChProfileSerializer(SelectProfileFieldsModelSerializer):
#     class Meta:
#         model = ChProfile
#         fields = ('user', 'last_login', 'public_name', 'first_name', 'last_name', 'sex', 'birth_date',
#                   '_languages', 'timezone', 'country', 'region', 'city', 'private_status', 'public_status',
#                   'personal_color', 'picture', 'avatar', 'private_show_age', 'public_show_age', 'public_show_location',
#                   'public_show_sex')
#
#
# class ChProfileLevel0Serializer(SelectProfileFieldsModelSerializer):
#
#     class Meta:
#         model = ChProfile
#         fields = ('user', 'public_name', 'avatar', 'personal_color', 'first_name', 'last_name', 'picture', )
#
#
#
# class ChProfileLevel1Serializer(SelectProfileFieldsModelSerializer):
#
#     user = serializers.SlugRelatedField(read_only=True, slug_field='username', allow_null=False)
#     city = serializers.SlugRelatedField(read_only=True, slug_field='name', )  # TODO: read only??
#     region = serializers.SlugRelatedField(read_only=True, slug_field='name')  # TODO: read only??
#     country = serializers.SlugRelatedField(read_only=True, slug_field='name')  # TODO: read only??
#     languages = serializers.SlugRelatedField(many=True, read_only=True, slug_field='language')  # TODO: read only??
#
#     # Hive subscriptions (and not only hive of which he is the creator)
# #    hives = serializers.SlugRelatedField(many=True, slug_field='slug')
#
#     class Meta:
#         model = ChProfile
#         fields = ('user', 'last_login', 'public_name', 'first_name', 'last_name', 'sex', 'birth_date',
#                   'languages', 'timezone', 'country', 'region', 'city', 'private_status', 'public_status',
#                   'personal_color', 'picture', 'avatar', 'private_show_age', 'public_show_age', 'public_show_location',
#                   'public_show_sex')


# ============================================================ #
#                        Hives & Chats                         #
# ============================================================ #
class ChChatLevel2Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET hive info,
       Used by the following serializers: ChPublicChatLevel3Serializer, ChCommunityPublicChatLevel3Serializer

    """
    last_message = ChMessageLevel1Serializer(many=False, read_only=True)

    class Meta:
        model = ChChat
        fields = ('chat_id', 'count', 'created', 'slug', 'type', 'last_message')


class ChCommunityPublicChatLevel4Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET chat info,

    """

    moderators = serializers.SlugRelatedField(many=True, slug_field='public_name', read_only=True)
    chat = ChChatLevel2Serializer(many=False, read_only=True)

    class Meta:
        model = ChCommunityPublicChat
        fields = ('name', 'description', 'moderators', 'rules', 'picture', 'chat')


class ChPublicChatLevel4Serializer(serializers.ModelSerializer):
    chat = ChChatLevel2Serializer(many=False, read_only=True)

    class Meta:
        model = ChPublicChat
        fields = ('chat', )


class ChHiveLevel1Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET hive list,

    """
    category = serializers.SlugRelatedField(read_only=True, slug_field='code')
    languages = serializers.SlugRelatedField(source='_languages', many=True, read_only=True, slug_field='language')

    # If in the POST we only need to establish the relationship with User model (not update the model itself) we
    # set read_only to True
    creator = serializers.SlugRelatedField(read_only=True, slug_field='public_name')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag')
    public_chat = ChPublicChatLevel1Serializer(many=False, read_only=True)
    community_public_chats = ChCommunityPublicChatListLevel1Serializer(many=True, read_only=True)

    subscribed_users_count = serializers.IntegerField(source='get_subscribed_users_count', read_only=True)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass

        fields_to_remove = kwargs.pop('fields_to_remove', None)

        # Instantiate the superclass normally
        super(ChHiveLevel1Serializer, self).__init__(*args, **kwargs)

        if fields_to_remove is not None:
            # Drop fields that are specified in the `fields` argument.
            for field_name in fields_to_remove:
                self.fields.pop(field_name)

    class Meta:
        model = ChHive
        fields = ('name', 'slug', 'description', 'creation_date', 'priority', 'type', 'category', 'languages',
                  'creator', 'tags', 'subscribed_users_count', 'public_chat', 'community_public_chats', 'admins')


class ChChatListLevel2Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET chat list,

    """
    last_message = ChMessageLevel1Serializer(many=False, read_only=True)

    class Meta:
        model = ChChat
        fields = ('chat_id', 'slug', 'type', 'last_message')


class ChHiveSerializer(serializers.ModelSerializer):
    """Used by the following API methods: GET hive info,

    """
    category = serializers.SlugRelatedField(read_only=True, slug_field='code')
    languages = serializers.SlugRelatedField(source='_languages', many=True, read_only=True, slug_field='language')

    # If in the POST we only need to establish the relationship with User model (not update the model itself) we
    # set read_only to True
    creator = serializers.SlugRelatedField(read_only=True, slug_field='public_name')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag')
    public_chat = ChPublicChatLevel4Serializer(many=False, read_only=True)
    community_public_chats = ChCommunityPublicChatLevel4Serializer(many=True, read_only=True)
    community = ChCommunityLevel1Serializer(many=False, read_only=True)

    subscribed_users_count = serializers.IntegerField(source='get_subscribed_users_count', read_only=True)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass

        fields_to_remove = kwargs.pop('fields_to_remove', None)

        # Instantiate the superclass normally
        super(ChHiveSerializer, self).__init__(*args, **kwargs)

        if fields_to_remove is not None:
            # Drop fields that are specified in the `fields` argument.
            for field_name in fields_to_remove:
                self.fields.pop(field_name)

    class Meta:
        model = ChHive
        fields = ('languages', 'category', 'chprofile_set', 'creation_date', 'creator', 'description',
                  'name', 'priority', 'rules', 'slug', 'tags', 'type', 'subscribed_users_count', 'public_chat',
                  'community_public_chats', 'community')


class ChChatLevel3Serializer(serializers.ModelSerializer):
    """Used by the following API methods: GET chat info,

    """
    community = ChCommunityPublicChatLevel1Serializer(read_only=True)

    class Meta:
        model = ChChat
        fields = ('chat_id', 'community', 'count', 'created', 'type')


class ChMessageSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(read_only=True, slug_field='public_name')
    id = serializers.IntegerField(source='_count', read_only=True)

    class Meta:
        model = ChMessage
        fields = ('id', 'received', 'content', 'content_type', 'created', 'profile')