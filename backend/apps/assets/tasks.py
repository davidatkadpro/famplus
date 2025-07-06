from celery import shared_task

from .models import Asset
from .services import get_price_for_asset


@shared_task
def fetch_latest_prices():
    """Fetch current prices for all assets from CoinGecko."""
    for asset in Asset.objects.all():
        get_price_for_asset(asset, force=True)
    return "ok"
