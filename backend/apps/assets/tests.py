from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from apps.accounting.models import Account, Transaction
from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .gains import calculate_gain, gain_for_asset
from .models import Asset, AssetTransactionLink, Price
from .services import fetch_price_for_symbol, get_price_for_asset
from .tasks import fetch_latest_prices


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


class PriceServiceTests(TestCase):
    @patch("apps.assets.services.requests.get")
    def test_fetch_price_for_symbol(self, mock_get):
        mock_get.return_value.json.return_value = {"bitcoin": {"usd": 123.45}}
        mock_get.return_value.raise_for_status.return_value = None
        price = fetch_price_for_symbol("bitcoin")
        self.assertEqual(price, Decimal("123.45"))

    @patch("apps.assets.services.fetch_price_for_symbol")
    def test_get_price_for_asset_cached(self, mock_fetch):
        family = Family.objects.create(
            name="F", owner=User.objects.create_user("a@b.com")
        )
        asset = Asset.objects.create(
            family=family,
            name="Coin",
            symbol="coin",
            current_price=Decimal("2"),
            price_fetched_at=timezone.now(),
        )
        price = get_price_for_asset(asset)
        self.assertEqual(price, Decimal("2"))
        mock_fetch.assert_not_called()

    @patch("apps.assets.services.fetch_price_for_symbol")
    def test_get_price_for_asset_refresh(self, mock_fetch):
        family = Family.objects.create(
            name="F2", owner=User.objects.create_user("b@b.com")
        )
        asset = Asset.objects.create(
            family=family,
            name="Coin",
            symbol="coin",
            current_price=Decimal("1"),
            price_fetched_at=timezone.now() - timedelta(hours=2),
        )
        mock_fetch.return_value = Decimal("3")
        price = get_price_for_asset(asset)
        self.assertEqual(price, Decimal("3"))
        asset.refresh_from_db()
        self.assertEqual(asset.current_price, Decimal("3"))


class GainComputationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user2@example.com", "pass")
        self.family = Family.objects.create(name="Smiths", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )

    def test_calculate_gain_fifo(self):
        txs = [
            (Decimal("1"), Decimal("10")),
            (Decimal("1"), Decimal("20")),
            (-Decimal("1.5"), Decimal("30")),
        ]
        gain = calculate_gain(txs, "fifo")
        self.assertEqual(gain, Decimal("25"))

    def test_gain_for_asset(self):
        asset = Asset.objects.create(family=self.family, name="Coin", symbol="c")
        debit = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        credit = Account.objects.create(
            family=self.family, name="Crypto", type=Account.Type.ASSET
        )
        buy1 = Transaction.objects.create(
            family=self.family,
            description="b1",
            amount="10",
            debit_account=debit,
            credit_account=credit,
        )
        AssetTransactionLink.objects.create(
            family=self.family, asset=asset, transaction=buy1, quantity="1"
        )
        buy2 = Transaction.objects.create(
            family=self.family,
            description="b2",
            amount="20",
            debit_account=debit,
            credit_account=credit,
        )
        AssetTransactionLink.objects.create(
            family=self.family, asset=asset, transaction=buy2, quantity="1"
        )
        sell = Transaction.objects.create(
            family=self.family,
            description="s",
            amount="30",
            debit_account=credit,
            credit_account=debit,
        )
        AssetTransactionLink.objects.create(
            family=self.family, asset=asset, transaction=sell, quantity="-1.5"
        )
        gain = gain_for_asset(asset, "fifo")
        self.assertEqual(gain, Decimal("25"))

    @patch("apps.assets.services.fetch_price_for_symbol")
    def test_fetch_latest_prices_task(self, mock_fetch):
        asset = Asset.objects.create(family=self.family, name="Coin", symbol="coin")
        mock_fetch.return_value = Decimal("1")
        fetch_latest_prices()
        asset.refresh_from_db()
        self.assertEqual(asset.current_price, Decimal("1"))
        self.assertTrue(asset.prices.filter(value="1").exists())


class AssetAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("parent2@example.com", "pass")
        self.family = Family.objects.create(name="Cooper", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )
        self.client.force_authenticate(user=self.user)

    def test_assets_include_current_price(self):
        asset = Asset.objects.create(
            family=self.family,
            name="Bitcoin",
            symbol="BTC",
            current_price=Decimal("123.45"),
        )

        resp = self.client.get("/api/assets/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]["id"], asset.id)
        self.assertEqual(resp.data[0]["current_price"], "123.4500")

    def test_filter_asset_prices_by_asset(self):
        asset1 = Asset.objects.create(family=self.family, name="A1", symbol="A1")
        asset2 = Asset.objects.create(family=self.family, name="A2", symbol="A2")
        Price.objects.create(
            family=self.family, asset=asset1, value="1", timestamp=timezone.now()
        )
        Price.objects.create(
            family=self.family, asset=asset2, value="2", timestamp=timezone.now()
        )

        resp = self.client.get(f"/api/asset-prices/?asset={asset1.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["asset"], asset1.id)
