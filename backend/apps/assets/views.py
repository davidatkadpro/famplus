from apps.families.mixins import FamilyQuerySetMixin
from rest_framework import permissions, viewsets

from .models import Asset, AssetTransactionLink, Price, ExchangeOrder, ExchangeTrade
from .serializers import (
    AssetSerializer,
    AssetTransactionLinkSerializer,
    PriceSerializer,
    ExchangeOrderSerializer,
    ExchangeTradeSerializer,
)
from .services import match_orders


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


# ===== Virtual Exchange ViewSets =====


class ExchangeOrderViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = ExchangeOrder.objects.all().order_by("-created_at")
    serializer_class = ExchangeOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().select_related("asset")
        asset_id = self.request.query_params.get("asset")
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        if self.request.query_params.get("book") == "1":
            # Public order book: only open/partial orders for the asset
            return qs.filter(status__in=[ExchangeOrder.OPEN, ExchangeOrder.PARTIAL])

        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(
            family=self.request.user.membership_set.first().family,
            user=self.request.user,
            remaining=serializer.validated_data["quantity"],
        )
        # Attempt to match immediately
        match_orders(order)


class ExchangeTradeViewSet(FamilyQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ExchangeTrade.objects.all().order_by("-timestamp")
    serializer_class = ExchangeTradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().select_related("asset")
        asset_id = self.request.query_params.get("asset")
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs
