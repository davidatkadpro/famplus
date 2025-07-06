from apps.families.mixins import FamilyQuerySetMixin
from rest_framework import permissions, viewsets

from .models import Asset, AssetTransactionLink, Price
from .serializers import (
    AssetSerializer,
    AssetTransactionLinkSerializer,
    PriceSerializer,
)


class AssetViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by("id")
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)


class PriceViewSet(FamilyQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Price.objects.all().order_by("-timestamp")
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        asset_id = self.request.query_params.get("asset")
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs


class AssetTransactionLinkViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = AssetTransactionLink.objects.all().order_by("id")
    serializer_class = AssetTransactionLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)
