"""API views for the families app."""

from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import Family
from .serializers import FamilySerializer


class IsFamilyOwner(permissions.BasePermission):
    """Allow access only to family owners."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class FamilyViewSet(viewsets.ModelViewSet):
    """CRUD for families with membership-based filtering."""

    serializer_class = FamilySerializer

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            perms = [permissions.IsAuthenticated, IsFamilyOwner]
        else:
            from .permissions import IsFamilyMember

            perms = [permissions.IsAuthenticated, IsFamilyMember]
        return [p() for p in perms]

    def perform_create(self, serializer):
        from .models import Membership

        family = serializer.save(owner=self.request.user)
        Membership.objects.create(
            user=self.request.user,
            family=family,
            role=Membership.Role.PARENT,
        )

    def get_queryset(self):
        user = self.request.user
        return (
            Family.objects.filter(Q(owner=user) | Q(memberships__user=user))
            .distinct()
            .order_by("id")
        )
