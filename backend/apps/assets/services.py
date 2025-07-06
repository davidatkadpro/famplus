from datetime import timedelta
from decimal import Decimal
from typing import Optional

import requests
from django.utils import timezone

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
