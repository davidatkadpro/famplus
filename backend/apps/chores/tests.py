from datetime import date

from apps.accounting.models import Account, Transaction
from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Chore, Entry
from .services import exchange_points, get_user_points
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

    def test_reject_entry(self):
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
        response = self.client.post(f"/api/chore-entries/{entry.id}/reject/")
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.status, Entry.Status.REJECTED)

    def test_exchange_points_service(self):
        chore = Chore.objects.create(
            family=self.family,
            name="Dust",
            schedule="daily",
            points=5,
        )

        Entry.objects.create(
            family=self.family,
            chore=chore,
            assigned_to=self.user,
            due_date=date.today(),
            status=Entry.Status.APPROVED,
        )
        cash = Account.objects.create(
            family=self.family, name="Cash", type=Account.Type.ASSET
        )
        exchange_points(self.user, cash, 5)
        self.assertEqual(get_user_points(self.user), 0)
        self.assertTrue(
            Transaction.objects.filter(description="Points exchange").exists()
        )

    def test_list_entries_scoped_by_family(self):
        other_user = User.objects.create_user("other@example.com", "pass")
        other_family = Family.objects.create(name="Jones", owner=other_user)
        Membership.objects.create(
            user=other_user, family=other_family, role=Membership.Role.PARENT
        )
        other_chore = Chore.objects.create(
            family=other_family, name="Mow", schedule="daily", points=1
        )
        Entry.objects.create(
            family=other_family,
            chore=other_chore,
            assigned_to=other_user,
            due_date=date.today(),
        )

        own_chore = Chore.objects.create(
            family=self.family, name="Sweep", schedule="daily", points=1
        )
        Entry.objects.create(
            family=self.family,
            chore=own_chore,
            assigned_to=self.user,
            due_date=date.today(),
        )

        resp = self.client.get("/api/chore-entries/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["chore"], own_chore.id)
