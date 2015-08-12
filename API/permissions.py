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
            ChHiveSubscription.objects.get(hive=obj.hive, profile=request.user.profile, subscription_state='active')
        except ChHiveSubscription.DoesNotExist:
            return False
        else:
            if obj.type == 'public':  # If it is a public chat it will be enough to check the user is subscribed to the hive
                return True
            else:
                try:  # For group and private chats we need the user to be or have been subscribed to this chat.
                    ChChatSubscription.objects.get(chat=obj, profile=request.user.profile)
                except ChChatSubscription.DoesNotExist:
                    return False
                else:
                    # TODO: We should add additional checks here, (blocked?, expelled from a group?)
                    return True


class CanGetProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("object permission is returning: ", obj.user == request.user)
        return obj.user == request.user


class CanGetHiveUsers(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            ChHiveSubscription.objects.get(hive=obj, profile=request.user.profile, subscription_state='active')
        except ChHiveSubscription.DoesNotExist:
            return False
        else:
            return True
