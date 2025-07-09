"""API views for the families app."""

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Family, Invitation, Membership
from .serializers import FamilySerializer, InvitationSerializer, MembershipSerializer


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


# === Invitation ===


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        family_id = self.request.query_params.get("family")
        qs = Invitation.objects.filter(family__memberships__user=self.request.user)
        if family_id:
            qs = qs.filter(family_id=family_id)
        return qs.order_by("-created")

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def accept(self, request, pk=None):
        inv = self.get_object()
        if inv.accepted:
            return Response({"detail": "Already accepted"}, status=400)
        inv.accept(request.user)
        return Response({"status": "accepted"})


# === Membership list (read-only) ===


class MembershipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        family_id = self.request.query_params.get("family")
        qs = Membership.objects.filter(family__memberships__user=self.request.user)
        if family_id:
            qs = qs.filter(family_id=family_id)
        return qs.select_related("user")
