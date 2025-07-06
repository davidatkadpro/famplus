"""Unit tests for the core app."""

from django.test import TestCase

from .models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user("test@example.com", "pass")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("pass"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser("admin@example.com", "pass")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
