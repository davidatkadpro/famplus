"""Basic tests for the families app."""

from apps.core.models import User
from django.test import TestCase
from rest_framework.test import APIClient

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


class FamilyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user("owner@example.com", "pass")
        self.other_user = User.objects.create_user("other@example.com", "pass")
        self.family = Family.objects.create(name="Smith", owner=self.owner)
        Membership.objects.create(
            user=self.owner, family=self.family, role=Membership.Role.PARENT
        )
        self.url = "/api/families/"

    def test_list_returns_only_member_families(self):
        other_family = Family.objects.create(name="Jones", owner=self.other_user)
        Membership.objects.create(
            user=self.other_user, family=other_family, role=Membership.Role.PARENT
        )

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.family.id)

    def test_cannot_access_non_member_family(self):
        other_family = Family.objects.create(name="Jones", owner=self.other_user)
        Membership.objects.create(
            user=self.other_user, family=other_family, role=Membership.Role.PARENT
        )

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"{self.url}{other_family.id}/")
        self.assertEqual(response.status_code, 404)
