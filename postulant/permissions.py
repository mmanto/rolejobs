from rest_framework import permissions

from choices import CV_COMPLETION


class IsItSelf(permissions.BasePermission):
    """
    Is the owner of his profile
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Only allow owners
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsCompletedProfile(permissions.BasePermission):
    """
    Only allow users with profile completed
    """
    message = "Profile is not completed"

    def has_object_permission(self, request, view, obj):
        return request.user.calculate_complete(CV_COMPLETION) == 100
