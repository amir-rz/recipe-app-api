from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'test@test.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_new_super_user(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            "test@test.com",
            "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # commented tests
    def cmnt_test_new_user_invalid_email(self):
        """ Test creating new user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create(email=None, password='test123')

    def cmnt_test_new_user_email_normalized(self):
        """ Test the email for a new user is normilized """
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create(
            email=email,
            password="test123"
        )

        self.assertEqual(user.email, email.lower())
