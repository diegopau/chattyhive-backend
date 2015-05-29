__author__ = 'diego'

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from core.models import ChUser, ChProfile, ChUserManager, ChChatSubscription, ChHiveSubscription,\
    ChHive, ChChat, ChMessage


# ================================================================== #
#                     Object-level permissions                       #
# ================================================================== #


class CanGetHiveList(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("object permission is returning: ", obj.user == request.user)
        return obj.user == request.user


class CanGetChatList(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("object permission is returning: ", obj.user == request.user)
        return obj.user == request.user


class CanGetChatMessages(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            ChChatSubscription.objects.get(chat=obj, profile=request.user.profile, deleted=False)
        except ChChatSubscription.DoesNotExist:
            return False
        else:
            return True


class CanGetHiveUsers(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            ChHiveSubscription.objects.get(hive=obj, profile=request.user.profile, deleted=False)
        except ChHiveSubscription.DoesNotExist:
            return False
        else:
            return True
