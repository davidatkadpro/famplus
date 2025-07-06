"""Basic tests for the families app."""

from apps.core.models import User
from django.test import TestCase

from .models import Family, Invitation, Membership


class FamiliesModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.user)

    def test_membership_creation(self):
        mem = Membership.objects.create(
            user=self.user, family=self.family, role=Membership.Role.PARENT
        )
        self.assertEqual(mem.family, self.family)
        self.assertEqual(mem.user, self.user)

    def test_invitation_accept(self):
        invite = Invitation.objects.create(
            email="child@example.com", family=self.family, role=Membership.Role.CHILD
        )
        new_user = User.objects.create_user("child@example.com", "pass")
        invite.accept(new_user)
        self.assertTrue(
            Membership.objects.filter(user=new_user, family=self.family).exists()
        )
        self.assertTrue(invite.accepted)
