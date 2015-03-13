from rest_framework import serializers
from core.models import ChUser, ChProfile


# Serializers define the API representation.
class ChUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChUser
        fields = ('date_joined', 'email', 'is_active', 'is_authenticated', 'is_staff', 'objects', 'related_device',
                  'username')


class ChProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChProfile
        fields = ('user', 'last_login', 'public_name', 'first_name', 'last_name', 'sex', 'birth_date',
                  '_languages', 'timezone', 'country', 'region', 'city', 'private_status', 'public_status',
                  'personal_color', 'photo', 'avatar', 'private_show_age', 'public_show_age', 'public_show_location',
                  'public_show_sex')