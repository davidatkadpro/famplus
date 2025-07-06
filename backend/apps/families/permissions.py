"""Custom DRF permissions for family scoped access."""

from rest_framework import permissions

from .models import Family, Membership


class IsFamilyMember(permissions.BasePermission):
    """Allow access if the user belongs to the object's family."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, Family):
            family = obj
        else:
            family = getattr(obj, "family", None)

        if family is None:
            return False

        return Membership.objects.filter(user=user, family=family).exists()

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class HasFamilyAccess(permissions.BasePermission):
    """Generic permission using an object's ``family`` attribute."""

    def has_object_permission(self, request, view, obj):
        family = getattr(obj, "family", None)
        if family is None:
            return False
        return Membership.objects.filter(user=request.user, family=family).exists()
