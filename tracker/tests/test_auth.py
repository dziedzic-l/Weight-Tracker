from django.test import TestCase
from django.contrib.auth import get_user_model


class TestAuth(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('user', 'user@gmail.com', 'pass')

    def test_login_with_correct_credentials(self):
        is_logged = self.client.login(username='user', password='pass')
        self.assertEqual(is_logged, True)

    def test_login_with_empty_credentials(self):
        is_logged = self.client.login(username='', password='')
        self.assertEqual(is_logged, False)

    def test_login_with_invalid_credentials(self):
        is_logged = self.client.login(username='user123', password='pass123')
        self.assertEqual(is_logged, False)

    def test_login_with_incorrect_username(self):
        is_logged = self.client.login(username='user123', password='pass')
        self.assertEqual(is_logged, False)

    def test_login_with_incorrect_password(self):
        is_logged = self.client.login(username='user', password='pass123')
        self.assertEqual(is_logged, False)
