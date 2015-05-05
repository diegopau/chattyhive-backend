__author__ = 'diego'

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission


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