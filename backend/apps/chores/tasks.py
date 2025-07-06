from datetime import date, timedelta

from celery import shared_task

from .models import Chore, Entry


@shared_task
def spawn_entries():
    """Create upcoming chore entries for active chores."""
    tomorrow = date.today() + timedelta(days=1)
    for chore in Chore.objects.filter(archived=False):
        Entry.objects.get_or_create(
            family=chore.family,
            chore=chore,
            assigned_to=chore.family.owner,
            due_date=tomorrow,
        )
