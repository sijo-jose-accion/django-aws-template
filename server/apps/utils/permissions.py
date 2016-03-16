__author__ = 'dkarchmer'

from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access (read/write)
    """

    def has_permission(self, request, view):

        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the snippet
        return obj is None or obj.created_by == request.user