from datetime import date

from apps.chores.models import Chore, Entry
from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Notification
from .tasks import send_due_chore_notifications


class NotificationsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )

    def test_due_chore_task_creates_notification(self):
        chore = Chore.objects.create(
            family=self.family, name="Sweep", schedule="daily", points=1
        )
        Entry.objects.create(
            family=self.family,
            chore=chore,
            assigned_to=self.user,
            due_date=date.today(),
        )
        send_due_chore_notifications()
        self.assertTrue(Notification.objects.filter(user=self.user).exists())


class NotificationsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("parent@example.com", "pass")
        self.family = Family.objects.create(name="Jones", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )
        self.client.force_authenticate(user=self.user)

    def test_mark_read(self):
        note = Notification.objects.create(user=self.user, message="hi")
        resp = self.client.post("/api/notifications/mark_read/", {"ids": [note.id]})
        self.assertEqual(resp.status_code, 200)
        note.refresh_from_db()
        self.assertTrue(note.read)
