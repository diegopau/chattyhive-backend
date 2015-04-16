from rest_framework import serializers
from core.models import ChUser, ChProfile, LanguageModel, TagModel, ChHive, ChChat, City, Region, Country


class LoginCredentialsSerializer(serializers.Serializer):
    """Serializer class used validate a public_name or email and a password

    """



    def validate(self, attrs):
        credentials = {
            self.username_field:

        }

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
