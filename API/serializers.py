from rest_framework import serializers, status
from rest_framework.response import Response
from core.models import ChUser, ChProfile, LanguageModel, TagModel, ChHive, ChChat, City, Region, Country
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, ValidationError
import re


class LoginCredentialsSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """
    email = serializers.EmailField()
    public_name = serializers.CharField(max_length=20, validators=[RegexValidator(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters and "_" are allowed.')])
    password = serializers.CharField(write_only=True)

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
        if 'email' in data:
            # We set to an empty string the param that is not inside the request body
            data['public_name'] = ''
            try:
                user = ChUser.objects.get(email=data['email'])
                # For security reasons we return a 401 instead of a 404 (we don't want to give clues of who is or who
                # is not registered in the service
            except ChUser.DoesNotExist:
                raise ValidationError("The ChUser object does not exist", code="401")
            data['username'] = user.username
        elif 'public_name' in data:
            data['email'] = ''
            try:
                profile = ChProfile.objects.select_related().get(public_name=data['public_name'])
            except ChProfile.DoesNotExist:
                raise ValidationError("The ChUser object, obtained from the profile, does not exist", code="401")
            data['username'] = profile.username
        else:
            raise serializers.ValidationError("No email or public_name specified")
        return data

    # We need a save() implementation to get an object instance from the view
    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']


# ============================================================ #
#                     Model Serializers                        #
# ============================================================ #

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ('language')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('tag')


# Serializers define the API representation.
class ChUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChUser
        fields = ('date_joined', 'email', 'is_active', 'is_authenticated', 'is_staff', 'objects', 'related_device',
                  'username')


class ChChatLevel0Serializer(serializers.ModelSerializer):
    class Meta:
        model = ChChat
        fields = ('count', 'type', 'hive', 'channel_unicode')


class ChProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChProfile
        fields = ('user', 'last_login', 'public_name', 'first_name', 'last_name', 'sex', 'birth_date',
                  '_languages', 'timezone', 'country', 'region', 'city', 'private_status', 'public_status',
                  'personal_color', 'photo', 'avatar', 'private_show_age', 'public_show_age', 'public_show_location',
                  'public_show_sex')


class ChProfileLevel1Serializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(read_only=True, slug_field='username', allow_null=False)
    city = serializers.SlugRelatedField(read_only=True, slug_field='name', )  # TODO: read only??
    region = serializers.SlugRelatedField(read_only=True, slug_field='name')  # TODO: read only??
    country = serializers.SlugRelatedField(read_only=True, slug_field='name')  # TODO: read only??
    languages = serializers.SlugRelatedField(many=True, read_only=True, slug_field='language')  # TODO: read only??

    # Hive subscriptions (and not only hive of which he is the creator)
#    hives = serializers.SlugRelatedField(many=True, slug_field='slug')

    class Meta:
        model = ChProfile
        fields = ('user', 'last_login', 'public_name', 'first_name', 'last_name', 'sex', 'birth_date',
                  'languages', 'timezone', 'country', 'region', 'city', 'private_status', 'public_status',
                  'personal_color', 'photo', 'avatar', 'private_show_age', 'public_show_age', 'public_show_location',
                  'public_show_sex')


class ChHiveSerializer(serializers.ModelSerializer):
    # Los únicos objetos que pueden llegar a tener que ser creados son los tags. El resto ya están creados yl o que se
    # hace es relacionarlos únicamente

    category = serializers.SlugRelatedField(read_only=True, slug_field='code')
    languages = serializers.SlugRelatedField(many=True, read_only=True, slug_field='language')
    creator = serializers.SlugRelatedField(read_only=True, slug_field='public_name')
    tags = TagSerializer(many=True)

    class Meta:
        model = ChHive
        fields = ('name', 'slug', 'description', 'category', 'languages', 'creator', 'creation_date', 'tags',
                  'priority', 'type')


class ChHiveLevel1Serializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(read_only=True, slug_field='code')
    languages = serializers.SlugRelatedField(many=True, read_only=True, slug_field='language')

    # If in the POST we only need to establish the relationship with User model (not update the model itself) we
    # set read_only to True
    creator = serializers.SlugRelatedField(read_only=True, slug_field='public_name')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag')

    class Meta:
        model = ChHive
        fields = ('name', 'slug', 'description', 'category', 'languages', 'creator', 'creation_date', 'tags',
                  'priority', 'type')
