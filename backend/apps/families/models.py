"""Models for the families app."""

from apps.core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


class FamilyScopedModel(TimeStampedModel):
    """Abstract base model carrying a ``family`` foreign key."""

    family = models.ForeignKey(
        "families.Family",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class Family(TimeStampedModel):
    """A group of users managed together."""

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_families",
    )
    settings_json = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name


class Membership(TimeStampedModel):
    """Link between a user and a family with a role."""

    class Role(models.TextChoices):
        PARENT = "parent", "Parent"
        CHILD = "child", "Child"
        GUEST = "guest", "Guest"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        unique_together = ("user", "family")

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.user} -> {self.family} ({self.role})"


class Invitation(TimeStampedModel):
    """Invitation to join a family."""

    email = models.EmailField()
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="invitations"
    )
    role = models.CharField(max_length=10, choices=Membership.Role.choices)
    code = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        default=lambda: get_random_string(32),
    )
    accepted = models.BooleanField(default=False)

    def accept(self, user: settings.AUTH_USER_MODEL):
        Membership.objects.create(user=user, family=self.family, role=self.role)
        self.accepted = True
        self.save(update_fields=["accepted"])

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"Invite {self.email} to {self.family}"  # type: ignore[str-format]
