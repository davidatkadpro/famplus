from apps.accounting.models import Transaction
from apps.families.models import FamilyScopedModel
from django.db import models


class Asset(FamilyScopedModel):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20)
    current_price = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    price_fetched_at = models.DateTimeField(null=True, blank=True)

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


class ExchangeOrder(FamilyScopedModel):
    BUY = "buy"
    SELL = "sell"
    SIDE_CHOICES = [(BUY, "Buy"), (SELL, "Sell")]

    OPEN = "open"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (OPEN, "Open"),
        (PARTIAL, "Partially filled"),
        (FILLED, "Filled"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="exchange_orders"
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="orders")
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)  # limit price
    remaining = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=OPEN, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return f"{self.side} {self.asset.symbol} {self.quantity} @ {self.price} ({self.status})"


class ExchangeTrade(FamilyScopedModel):
    buy_order = models.ForeignKey(
        ExchangeOrder,
        on_delete=models.CASCADE,
        related_name="trades_as_buy",
    )
    sell_order = models.ForeignKey(
        ExchangeOrder,
        on_delete=models.CASCADE,
        related_name="trades_as_sell",
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="trades")
    price = models.DecimalField(max_digits=12, decimal_places=4)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return f"Trade {self.quantity} {self.asset.symbol} @ {self.price}"
