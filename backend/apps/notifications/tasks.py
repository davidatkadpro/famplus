from datetime import date

from apps.chores.models import Entry
from celery import shared_task

from .models import Notification


@shared_task
def send_due_chore_notifications():
    """Notify users of chores due today."""
    today = date.today()
    for entry in Entry.objects.filter(due_date=today, status=Entry.Status.AWAITING):
        Notification.objects.create(
            user=entry.assigned_to,
            message=f"Chore '{entry.chore.name}' is due today!",
        )
    return "ok"
