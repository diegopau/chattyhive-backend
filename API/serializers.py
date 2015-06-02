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


class AsyncServices(serializers.Serializer):

    name = serializers.CharField(max_length=20)
    app = serializers.CharField(max_length=255, allow_blank=True)
    reg_id = serializers.CharField(max_length=255, allow_blank=True)

    def validate(self, data):
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        name = self.validated_data['name']
        app = self.validated_data['app']
        reg_id = self.validated_data['reg_id']


class LoginCredentialsSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """
    email = serializers.EmailField()
    public_name = serializers.CharField(
        max_length=20, validators=[RegexValidator(r'^[0-9a-zA-Z_]+$',
                                                  'Only alphanumeric characters and "_" are allowed.')])
    password = serializers.CharField(write_only=True)
    dev_os = serializers.CharField(max_length=20)
    dev_type = serializers.CharField(max_length=20)
    dev_code = serializers.CharField(max_length=16, allow_blank=True)
    dev_id = serializers.CharField(max_length=50)
    services = AsyncServices(many=True)

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
        DEV_TYPE_CHOICES = ('smartphone', '6-8tablet', 'big_tablet', 'netbook', 'laptop', 'desktop',
                            'big_screen_desktop', 'tv')

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

        for service in data['services']:
            if service['name'] == 'gcm':
                if data['dev_os'] != 'android':
                    raise ValidationError("gcm service should never be specified if dev_os is not android", code="400")
                if 'app' in service:
                    if service['app'] == "":
                        raise ValidationError("app field for gcm can not be empty", code="400")
                    elif service['app'] not in settings.ALLOWED_GCM_APP_IDS:
                        raise ValidationError("app id for gcm not allowed", code="400")
                else:
                    raise ValidationError("app id is missing for gcm service", code="400")

                if 'reg_id' in service:
                    if service['reg_id'] == "":
                        raise ValidationError("app field for gcm can not be empty", code="400")

        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        dev_os = self.validated_data['dev_os']
        dev_type = self.validated_data['dev_type']
        dev_code = self.validated_data['dev_code']
        dev_id = self.validated_data['dev_id']
        services = self.validated_data['services']


class CheckAsyncServices(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """

    dev_id = serializers.CharField(
        max_length=50, validators=[RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$'))])
    dev_os = serializers.CharField(max_length=20)
    services = AsyncServices(many=True)

    def validate(self, data):
        DEV_OS_CHOICES = ('android', 'ios', 'wp', 'browser', 'windows', 'linux', 'mac')

        if 'dev_os' in data:
            if data['dev_os'] not in DEV_OS_CHOICES:
                raise ValidationError("Wrong dev_os", code="400")
        else:
            raise ValidationError("dev_os field is missing", code="400")

        for service in data['services']:
            if service['name'] == 'gcm':
                if data['dev_os'] != 'android':
                    raise ValidationError("gcm service should never be specified if dev_os is not android", code="400")
                if 'app' in service:
                    if service['app'] == "":
                        raise ValidationError("app field for gcm can not be empty", code="400")
                    elif service['app'] not in settings.ALLOWED_GCM_APP_IDS:
                        raise ValidationError("app id for gcm not allowed", code="400")
                else:
                    raise ValidationError("app id is missing for gcm service", code="400")

                if 'reg_id' in service:
                    if service['reg_id'] == "":
                        raise ValidationError("app field for gcm can not be empty", code="400")
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        dev_id = self.validated_data['dev_id']
        dev_os = self.validated_data['dev_os']
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
            if data['channel_name'].startswith('presence-'):
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
    dev_id = serializers.CharField(
        max_length=50, validators=[RegexValidator(re.compile('^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$'))])
    socket_id = serializers.CharField(max_length=255)

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
        if data['socket_id'] == '':
            raise ValidationError("Socket_id can not be a empty string", code="400")
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


#Serializers define the API representation.
class ChUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChUser
        fields = ('date_joined', 'email', 'is_active', 'is_authenticated', 'is_staff', 'objects', 'related_device',
                  'username')


class ChUserLevel0Serializer(serializers.ModelSerializer):
    class Meta:
        model = ChUser
        fields = ('email', 'username')


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
    """Used by the following API methods: GET hive list, ChProfileSerializer

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
                  'creator', 'tags', 'subscribed_users_count', 'public_chat', 'community_public_chats',)


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
        fields = ('name', 'languages', 'category', 'creation_date', 'creator', 'description',
                  'priority', 'rules', 'slug', 'tags', 'type', 'subscribed_users_count', 'public_chat',
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


# ============================================================ #
#                       Users & Profiles                       #
# ============================================================ #

class ChProfileSerializer(serializers.ModelSerializer):
    """Used by the following API methods: GET user profile,
       Used by the following serializers: --

    """

    user = ChUserLevel0Serializer(many=False, read_only=True)
    languages = serializers.SlugRelatedField(source='_languages', many=True, read_only=True, slug_field='language')
    country = serializers.SlugRelatedField(read_only=True, slug_field='code2')
    region = serializers.SlugRelatedField(read_only=True, slug_field='name_ascii')
    city = serializers.SlugRelatedField(read_only=True, slug_field='name_ascii')
    location = serializers.CharField(source='get_location', read_only=True)

    hives = ChHiveLevel1Serializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        profile_type = kwargs.pop('type', None)
        profile_package = kwargs.pop('package', None)

        TYPE_CHOICES = ('public', 'private', 'logged_profile')
        PACKAGE_CHOICES = ('basic', 'info', 'hives', 'complete')

        if profile_type is not None:
            if profile_type not in TYPE_CHOICES:
                raise ValidationError("Wrong type", code="400")
        else:
            raise ValidationError("profile_type is missing", code="400")

        if profile_package is not None:
            if profile_package not in PACKAGE_CHOICES:
                raise ValidationError("Wrong package", code="400")
        else:
            raise ValidationError("profile_package is missing", code="400")

        # Instantiate the superclass normally
        super(ChProfileSerializer, self).__init__(*args, **kwargs)

        # In the related ModelSerializers we will set all possible fields, with this code we will dynamically
        # drop some of these fields depending on the url path params and the query params of the client request
        allowed_fields = set()
        basic_fields = set()
        info_fields = set()
        hives_fields = set()

        if profile_type == 'logged_profile':

            basic_fields = {'user', 'public_name', 'avatar', 'personal_color', 'public_status', 'email',
                            'first_name', 'last_name', 'picture', 'private_status'}
            info_fields = {'birth_date', 'sex',
                           'languages', 'country', 'region', 'city', 'location', 'public_show_age', 'public_show_sex'
                           'public_show_location', 'private_show_age', 'private_show_location'}
            hives_fields = {'hives'}

        elif profile_type == 'public':

            basic_fields = {'public_name', 'avatar', 'personal_color', 'public_status'}
            info_fields = {'birth_date', 'sex', 'languages', 'country', 'region', 'city', 'location'}
            hives_fields = {'hives'}

        elif profile_type == 'private':

            pass  # TODO: private profiles code

        else:
            raise URLParamsError("Incorrect profile type specified", errors={})

        if profile_package == 'basic':
            allowed_fields = basic_fields
        elif profile_package == 'info':
            allowed_fields = info_fields
        elif profile_package == 'hives':
            allowed_fields = hives_fields
        elif profile_package == 'complete':
            allowed_fields = basic_fields | info_fields | hives_fields
        else:
            raise URLParamsError("The profile_package value doesn't match any API defined value", errors={})

        if allowed_fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            existing = set(self.fields.keys())
            for field_name in existing - allowed_fields:
                self.fields.pop(field_name)

    class Meta:
        model = ChProfile
        fields = ('user',  'public_name', 'avatar', 'personal_color', 'public_status', 'first_name',
                  'last_name', 'picture', 'private_status', 'birth_date', 'sex', 'languages', 'country', 'region',
                  'location', 'city', 'hives', 'public_show_age', 'public_show_location', 'public_show_sex',
                  'private_show_age', 'private_show_location', 'created', 'last_activity')
