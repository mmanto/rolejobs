# encoding=utf-8

from __future__ import unicode_literals

from rest_framework import permissions


class IsOwnJob(permissions.BasePermission):
    """
    If the user has permissions on the job
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner.user == request.user


class IsOfOwnJob(permissions.BasePermission):
    """
    If the element is related to user's own job
    """

    def has_object_permission(self, request, view, obj):
        return obj.job.owner.user == request.user


class IsOfOwnPostulation(permissions.BasePermission):
    """
    If the element is related to user's own postulation job
    """

    def has_object_permission(self, request, view, obj):
        return obj.postulation.job.owner.user == request.user
