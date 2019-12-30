from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from measures.views import (annual_measures, daily_measures, monthly_measures,
                            register)


class LoginUrlTest(SimpleTestCase):
    def test_login_page_status_code(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, LoginView.__name__)


class RegisterUrlTest(SimpleTestCase):
    def test_register_page_status_code(self):
        response = self.client.get('/register')
        self.assertEquals(response.status_code, 200)

    def test_register_page_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)


class MeasureUrlTest(TestCase):
    def auth_user(self):
        User = get_user_model()
        User.objects.create_user('user', 'user@gmail.com', 'pass')
        self.client.login(username='user', password='pass')

    def test_annual_measures_status_code(self):
        self.auth_user()
        response = self.client.get('/api/measures')
        self.assertEquals(response.status_code, 200)

    def test_annual_measures_is_resolved(self):
        url = reverse('annual-measures')
        self.assertEquals(resolve(url).func.__name__, annual_measures.__name__)

    def test_monthly_measures_status_code(self):
        self.auth_user()
        response = self.client.get('/api/measures/2019')
        self.assertEquals(response.status_code, 200)

    def test_monthly_measures_is_resolved(self):
        url = reverse('monthly-measures', args=[2019])
        self.assertEquals(resolve(url).func.__name__, monthly_measures.__name__)

    def test_daily_measures_status_code(self):
        self.auth_user()
        response = self.client.get('/api/measures/2019/11')
        self.assertEquals(response.status_code, 200)

    def test_daily_measures_is_resolved(self):
        url = reverse('daily-measures', args=[2019, 11])
        self.assertEquals(resolve(url).func.__name__, daily_measures.__name__)
