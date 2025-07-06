"""URL configuration for the project."""

from apps.families.views import FamilyViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("families", FamilyViewSet, basename="family")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
