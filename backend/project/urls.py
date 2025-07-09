"""URL configuration for the project."""

from apps.accounting.views import (
    AccountViewSet,
    CategoryViewSet,
    JournalViewSet,
    TransactionViewSet,
)
from apps.assets.views import (
    AssetTransactionLinkViewSet,
    AssetViewSet,
    PriceViewSet,
    ExchangeOrderViewSet,
    ExchangeTradeViewSet,
)
from apps.chores.views import ChoreViewSet, EntryViewSet
from apps.families.views import FamilyViewSet, InvitationViewSet, MembershipViewSet
from apps.notifications.views import NotificationViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("families", FamilyViewSet, basename="family")
router.register("family-invitations", InvitationViewSet, basename="invitation")
router.register("family-memberships", MembershipViewSet, basename="membership")
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
router.register("notifications", NotificationViewSet, basename="notification")
router.register("exchange-orders", ExchangeOrderViewSet, basename="exchangeorder")
router.register("exchange-trades", ExchangeTradeViewSet, basename="exchangetrade")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
