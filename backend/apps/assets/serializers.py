from rest_framework import serializers

from .models import Asset, AssetTransactionLink, Price, ExchangeOrder, ExchangeTrade


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name", "symbol", "current_price"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "asset", "value", "timestamp"]


class AssetTransactionLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTransactionLink
        fields = ["id", "asset", "transaction", "quantity"]


# === Virtual Exchange serializers ===

class ExchangeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeOrder
        fields = [
            "id",
            "asset",
            "side",
            "quantity",
            "price",
            "remaining",
            "status",
            "created_at",
        ]
        read_only_fields = ["remaining", "created_at"]


class ExchangeTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeTrade
        fields = [
            "id",
            "asset",
            "price",
            "quantity",
            "timestamp",
            "buy_order",
            "sell_order",
        ]
        read_only_fields = fields
