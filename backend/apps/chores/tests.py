from datetime import date

from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Chore, Entry
from .tasks import spawn_entries


class ChoreModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )

    def test_entry_creation(self):
        chore = Chore.objects.create(
            family=self.family, name="Wash dishes", schedule="daily", points=1
        )
        entry = Entry.objects.create(
            family=self.family,
            chore=chore,
            assigned_to=self.user,
            due_date=date.today(),
        )
        self.assertEqual(entry.chore, chore)
        self.assertEqual(entry.status, Entry.Status.AWAITING)

    def test_spawn_entries_task(self):
        Chore.objects.create(
            family=self.family, name="Vacuum", schedule="daily", points=2
        )
        spawn_entries()
        self.assertTrue(Entry.objects.filter(chore__name="Vacuum").exists())


class ChoreAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("parent@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)
        Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )
        self.client.force_authenticate(user=self.user)

    def test_approve_entry(self):
        chore = Chore.objects.create(
            family=self.family,
            name="Sweep",
            schedule="daily",
            points=1,
        )
        entry = Entry.objects.create(
            family=self.family,
            chore=chore,
            assigned_to=self.user,
            due_date=date.today(),
        )
        response = self.client.post(f"/api/chore-entries/{entry.id}/approve/")
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.status, Entry.Status.APPROVED)
