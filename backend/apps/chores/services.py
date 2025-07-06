"""Utility functions for chore point exchange."""

from decimal import Decimal

from apps.accounting.models import Account, Transaction
from django.db.models import Sum

from .models import Entry, PointExchange


def get_user_points(user) -> int:
    """Return approved points minus already exchanged points."""
    approved = (
        Entry.objects.filter(assigned_to=user, status=Entry.Status.APPROVED).aggregate(
            total=Sum("chore__points")
        )["total"]
        or 0
    )
    exchanged = (
        PointExchange.objects.filter(user=user).aggregate(total=Sum("points"))["total"]
        or 0
    )
    return int(approved) - int(exchanged)


def exchange_points(user, account: Account, points: int) -> Transaction:
    """Convert points to dollars and create accounting transaction."""
    available = get_user_points(user)
    if points > available:
        raise ValueError("Not enough points")

    expense_account, _ = Account.objects.get_or_create(
        family=account.family, name="Points Expense", type=Account.Type.EXPENSE
    )
    tx = Transaction.objects.create(
        family=account.family,
        description="Points exchange",
        amount=Decimal(points),
        debit_account=account,
        credit_account=expense_account,
    )
    PointExchange.objects.create(
        family=account.family, user=user, points=points, transaction=tx
    )
    return tx
