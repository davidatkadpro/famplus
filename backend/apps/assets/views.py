from rest_framework import permissions, viewsets

from .models import Asset, Price, AssetTransactionLink
from .serializers import (
    AssetSerializer,
    PriceSerializer,
    AssetTransactionLinkSerializer,
)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by("id")
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)


class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Price.objects.all().order_by("-timestamp")
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssetTransactionLinkViewSet(viewsets.ModelViewSet):
    queryset = AssetTransactionLink.objects.all().order_by("id")
    serializer_class = AssetTransactionLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)
