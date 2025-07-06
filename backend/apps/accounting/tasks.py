from celery import shared_task


@shared_task
def daily_summary():
    """Placeholder task updating account balances."""
    return "ok"
