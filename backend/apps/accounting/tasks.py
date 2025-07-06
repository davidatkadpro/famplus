from decimal import Decimal

from celery import shared_task

from .models import Account, Transaction


@shared_task
def daily_summary():
    """Placeholder task updating account balances."""
    return "ok"


@shared_task
def pay_monthly_interest():
    """Credit monthly interest to accounts with an interest rate."""
    for account in Account.objects.filter(interest_rate__gt=0):
        balance = account.balance
        if balance <= 0:
            continue
        interest = (Decimal(balance) * account.interest_rate).quantize(Decimal("0.01"))
        if interest <= 0:
            continue
        income_account, _ = Account.objects.get_or_create(
            family=account.family,
            name="Interest Income",
            type=Account.Type.INCOME,
        )
        Transaction.objects.create(
            family=account.family,
            description="Monthly Interest",
            amount=interest,
            debit_account=account,
            credit_account=income_account,
        )
    return "ok"
