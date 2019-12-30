from django.contrib.auth import get_user_model
from django.test import TestCase


class TestAuth(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('user', 'user@gmail.com', 'pass')

    def test_login(self):
        """Test authentication"""
        self.assertTrue(self.client.login(username='user', password='pass'))
        self.assertFalse(self.client.login(username='', password=''))
        self.assertFalse(self.client.login(username='us', password='pas'))
        self.assertFalse(self.client.login(username='user12', password='pass'))
        self.assertFalse(self.client.login(username='user', password='pass12'))
