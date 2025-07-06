from apps.accounting.models import Account, Transaction
from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase

from .models import Asset, AssetTransactionLink


class AssetsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )

    def test_link_transaction(self):
        asset = Asset.objects.create(family=self.family, name="Bitcoin", symbol="BTC")
        debit = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        credit = Account.objects.create(
            family=self.family, name="Crypto", type=Account.Type.ASSET
        )
        tx = Transaction.objects.create(
            family=self.family,
            description="Buy BTC",
            amount="10.00",
            debit_account=debit,
            credit_account=credit,
        )
        link = AssetTransactionLink.objects.create(
            family=self.family,
            asset=asset,
            transaction=tx,
            quantity="0.5",
        )
        self.assertEqual(link.asset, asset)
        self.assertEqual(link.transaction, tx)
