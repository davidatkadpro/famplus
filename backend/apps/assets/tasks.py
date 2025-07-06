from celery import shared_task


@shared_task
def fetch_latest_prices():
    """Placeholder task for price fetching."""
    return "ok"
