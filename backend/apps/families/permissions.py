"""Custom DRF permissions for family scoped access."""

from rest_framework import permissions

from .models import Membership


class IsFamilyMember(permissions.BasePermission):
    """Allows access only to members of a family."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        return Membership.objects.filter(user=user, family=obj).exists()
