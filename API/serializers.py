from rest_framework import serializers
from core.models import ChUser


# Serializers define the API representation.
class ChUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChUser
        fields = ('date_joined', 'email', 'is_active', 'is_authenticated', 'is_staff', 'objects', 'related_device',
                  'username')

