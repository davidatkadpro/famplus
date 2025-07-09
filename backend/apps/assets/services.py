from datetime import timedelta
from decimal import Decimal
from typing import Optional

import requests
from django.utils import timezone
from django.db import transaction as db_tx

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_price_for_symbol(symbol: str) -> Optional[Decimal]:
    """Return current USD price for a given CoinGecko symbol."""
    try:
        resp = requests.get(
            COINGECKO_URL,
            params={"ids": symbol.lower(), "vs_currencies": "usd"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        value = data.get(symbol.lower(), {}).get("usd")
        if value is None:
            return None
        return Decimal(str(value))
    except Exception:
        return None


def get_price_for_asset(
    asset, *, force: bool = False, stale_minutes: int = 60
) -> Optional[Decimal]:
    """Return price for asset using cached value if fresh."""
    if (
        not force
        and asset.current_price is not None
        and asset.price_fetched_at is not None
        and timezone.now() - asset.price_fetched_at < timedelta(minutes=stale_minutes)
    ):
        return asset.current_price

    value = fetch_price_for_symbol(asset.symbol)
    if value is None:
        return asset.current_price

    asset.current_price = value
    asset.price_fetched_at = timezone.now()
    asset.save(update_fields=["current_price", "price_fetched_at"])
    from .models import Price

    Price.objects.create(
        family=asset.family,
        asset=asset,
        value=value,
        timestamp=asset.price_fetched_at,
    )
    return value


# ===== Virtual exchange matching =====

def match_orders(order):
    """Attempt to match newly created order with opposing open orders.

    Matching rules:
    • BUY order matches lowest priced SELL orders where sell.price <= buy.price
    • SELL order matches highest priced BUY orders where buy.price >= sell.price
    • FIFO within same price (older orders fill first)
    """

    from .models import ExchangeOrder, ExchangeTrade

    if order.status != ExchangeOrder.OPEN:
        return

    side_opposite = ExchangeOrder.SELL if order.side == ExchangeOrder.BUY else ExchangeOrder.BUY

    # Build queryset of candidates
    qs = (
        ExchangeOrder.objects.filter(
            family=order.family,
            asset=order.asset,
            side=side_opposite,
            status__in=[ExchangeOrder.OPEN, ExchangeOrder.PARTIAL],
        )
    )

    if order.side == ExchangeOrder.BUY:
        qs = qs.filter(price__lte=order.price).order_by("price", "created_at")  # cheapest sells first
    else:
        qs = qs.filter(price__gte=order.price).order_by("-price", "created_at")  # highest buys first

    remaining = order.remaining

    with db_tx.atomic():
        for counter in qs.select_for_update():
            if remaining <= 0:
                break

            trade_qty = min(remaining, counter.remaining)
            trade_price = counter.price  # simple rule: use resting order price

            ExchangeTrade.objects.create(
                family=order.family,
                asset=order.asset,
                price=trade_price,
                quantity=trade_qty,
                buy_order=order if order.side == ExchangeOrder.BUY else counter,
                sell_order=counter if order.side == ExchangeOrder.BUY else order,
            )

            # Update remaining quantities
            counter.remaining -= trade_qty
            counter.status = (
                ExchangeOrder.FILLED if counter.remaining == 0 else ExchangeOrder.PARTIAL
            )
            counter.save(update_fields=["remaining", "status"])

            remaining -= trade_qty

        # Update the incoming order's state
        order.remaining = remaining
        order.status = (
            ExchangeOrder.FILLED if remaining == 0 else ExchangeOrder.PARTIAL
        )
        order.save(update_fields=["remaining", "status"])
