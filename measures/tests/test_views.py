from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from measures.models import Measure
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user', 'user@gmail.com', 'pass')
        self.user = User.objects.get(id=1)

    def test_register_view_GET(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        self.client.login(username='user', password='pass')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_register_view_POST(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'user2',
            'password1': 'strong!password',
            'password2': 'strong!password'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.get(id=2).username, 'user2')
        self.assertTrue(User.objects.get(id=1).is_authenticated)

    def test_home_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'measures/home.html')

    def test_measure_create_GET(self):
        url = reverse('measure-store')
        self.client.login(username='user', password='pass')
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'measures/home.html')

    def test_measure_create_POST(self):
        url = reverse('measure-store')
        self.client.login(username='user', password='pass')
        response = self.client.post(url, {
            'weight': 95,
            'date': '2019-11-13'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Measure.measures.all()[0].date, date(2019, 11, 13))
