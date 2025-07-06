from apps.accounting.models import Transaction
from apps.families.models import FamilyScopedModel
from django.db import models


class Asset(FamilyScopedModel):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.symbol


class Price(FamilyScopedModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="prices")
    value = models.DecimalField(max_digits=12, decimal_places=4)
    timestamp = models.DateTimeField()

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.asset} @ {self.timestamp}"  # type: ignore[str-format]


class AssetTransactionLink(FamilyScopedModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.quantity} {self.asset}"  # type: ignore[str-format]
