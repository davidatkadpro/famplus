"""URL configuration for the project."""

from apps.families.views import FamilyViewSet
from apps.chores.views import ChoreViewSet, EntryViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("families", FamilyViewSet, basename="family")
router.register("chores", ChoreViewSet, basename="chore")
router.register("chore-entries", EntryViewSet, basename="entry")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
