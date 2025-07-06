"""URL configuration for the project."""

from apps.families.views import FamilyViewSet
from apps.chores.views import ChoreViewSet, EntryViewSet
from apps.accounting.views import (
    AccountViewSet,
    CategoryViewSet,
    JournalViewSet,
    TransactionViewSet,
)
from apps.assets.views import (
    AssetViewSet,
    PriceViewSet,
    AssetTransactionLinkViewSet,
)
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("families", FamilyViewSet, basename="family")
router.register("chores", ChoreViewSet, basename="chore")
router.register("chore-entries", EntryViewSet, basename="entry")
router.register("accounts", AccountViewSet, basename="account")
router.register("categories", CategoryViewSet, basename="category")
router.register("journals", JournalViewSet, basename="journal")
router.register("transactions", TransactionViewSet, basename="transaction")
router.register("assets", AssetViewSet, basename="asset")
router.register("asset-prices", PriceViewSet, basename="price")
router.register(
    "asset-links",
    AssetTransactionLinkViewSet,
    basename="assettransactionlink",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
