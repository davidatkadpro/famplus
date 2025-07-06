from rest_framework import serializers

from .models import Asset, Price, AssetTransactionLink


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name", "symbol"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "asset", "value", "timestamp"]


class AssetTransactionLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTransactionLink
        fields = ["id", "asset", "transaction", "quantity"]
