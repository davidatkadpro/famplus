from apps.families.models import FamilyScopedModel
from django.conf import settings
from django.db import models


class Chore(FamilyScopedModel):
    """Template describing a scheduled task."""

    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=50)
    points = models.PositiveIntegerField(default=0)
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name


class Entry(FamilyScopedModel):
    """Individual occurrence of a chore assigned to a user."""

    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name="entries")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chore_entries",
    )
    due_date = models.DateField()

    class Status(models.TextChoices):
        AWAITING = "awaiting", "Awaiting"
        COMPLETED = "completed", "Completed"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        ACHIEVED = "achieved", "Achieved"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AWAITING
    )

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.chore} -> {self.assigned_to} on {self.due_date}"
