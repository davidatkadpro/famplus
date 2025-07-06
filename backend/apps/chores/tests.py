from datetime import date

from apps.core.models import User
from apps.families.models import Family, Membership
from django.test import TestCase

from .models import Chore, Entry


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
