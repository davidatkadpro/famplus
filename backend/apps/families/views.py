"""API views for the families app."""

from rest_framework import permissions, viewsets

from .models import Family
from .serializers import FamilySerializer


class IsFamilyOwner(permissions.BasePermission):
    """Allow access only to family owners."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class FamilyViewSet(viewsets.ModelViewSet):
    """CRUD for families."""

    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated, IsFamilyOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Family.objects.filter(owner=self.request.user)
