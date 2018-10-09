# encoding=utf-8

from __future__ import unicode_literals

from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    """
    Is employer user
    """

    def has_permission(self, request, view):
        return request.user.is_employer


class IsPostulant(permissions.BasePermission):
    """
    Is postulant user
    """

    def has_permission(self, request, view):
        return request.user.is_postulant
