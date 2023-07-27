from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User


# Tests for the class Usewr with hardcoded dafault_birthday

class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superpassword'
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertEqual(superuser.username, 'superuser')
        self.assertTrue(superuser.check_password('superpassword'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_age_calculation(self):
        # Assuming the default_birthday returns a date in 1970
        user = User(birthday=timezone.datetime(2000, 1, 1).date())
        self.assertEqual(user.age(), 23)

        # Test for age < 18
        user = User(birthday=timezone.datetime(2010, 1, 1).date())
        with self.assertRaises(ValidationError):
            user.clean()
