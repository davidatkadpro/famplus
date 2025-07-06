from decimal import Decimal

from apps.core.models import User
from apps.families.models import Family, Membership
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

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

    def test_account_balance(self):
        debit = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        credit = Account.objects.create(
            family=self.family, name="Income", type=Account.Type.INCOME
        )
        Transaction.objects.create(
            family=self.family,
            description="Payday",
            amount="50.00",
            debit_account=debit,
            credit_account=credit,
        )
        self.assertEqual(debit.balance, Decimal("50.00"))
        self.assertEqual(credit.balance, Decimal("-50.00"))

    def test_invalid_transaction_same_account(self):
        acct = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        with self.assertRaises(Exception):
            Transaction.objects.create(
                family=self.family,
                description="bad",
                amount="10.00",
                debit_account=acct,
                credit_account=acct,
            )


class AccountingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("parent@example.com", "pass")
        self.family = Family.objects.create(name="Jones", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )
        self.client.force_authenticate(user=self.user)
        self.debit = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        self.credit = Account.objects.create(
            family=self.family, name="Income", type=Account.Type.INCOME
        )

    def test_import_and_export_csv(self):
        csv_content = (
            "description,amount,debit_account,credit_account\n"
            f"Pay,20.00,{self.debit.id},{self.credit.id}\n"
        )
        file = SimpleUploadedFile(
            "tx.csv", csv_content.encode(), content_type="text/csv"
        )
        response = self.client.post("/api/transactions/import_csv/", {"file": file})
        self.assertEqual(response.status_code, 201)
        resp = self.client.get("/api/transactions/export_csv/")
        self.assertEqual(resp.status_code, 200)
        content = b"".join(resp.streaming_content).decode()
        self.assertIn("Pay", content)
