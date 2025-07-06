from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase

from .models import Account, Category, Journal, Transaction


class AccountingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )

    def test_create_transaction(self):
        debit = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        credit = Account.objects.create(
            family=self.family, name="Income", type=Account.Type.INCOME
        )
        category = Category.objects.create(family=self.family, name="Salary")
        journal = Journal.objects.create(family=self.family, date="2025-01-01")
        tx = Transaction.objects.create(
            family=self.family,
            description="Payday",
            amount="100.00",
            debit_account=debit,
            credit_account=credit,
            category=category,
            journal=journal,
        )
        self.assertEqual(tx.debit_account, debit)
        self.assertEqual(tx.credit_account, credit)
