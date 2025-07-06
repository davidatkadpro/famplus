from django.db.models import QuerySet


class FamilyQuerySetMixin:
    """Filter queryset by the authenticated user's current family."""

    family_lookup_field = "family"

    def get_family(self):
        membership = self.request.user.membership_set.first()
        return membership.family if membership else None

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        family = self.get_family()
        if family is None:
            return qs.none()
        return qs.filter(**{self.family_lookup_field: family})
