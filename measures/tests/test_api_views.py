import datetime

from django.contrib.auth.models import User
from measures.models import Measure
from django.urls import reverse

from rest_framework.test import APITestCase


class TestApiViews(APITestCase):
    def setUp(self):
        User.objects.create_user('user', 'user@gmail.com', 'pass')
        self.user = User.objects.get(id=1)
        self.client.login(username='user', password='pass')
        Measure.measures.create(
            user=self.user,
            weight=93,
            date=datetime.date(2019, 12, 30)
        )
        Measure.measures.create(
            user=self.user,
            weight=93,
            date=datetime.date(2018, 11, 2)
        )
        Measure.measures.create(
            user=self.user,
            weight=92,
            date=datetime.date(2019, 12, 29)
        )

    def test_annual_measures_GET(self):
        url = reverse('annual-measures')
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_monthly_measures_GET(self):
        url = reverse('monthly-measures', args=[2019])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_daily_measures_GET(self):
        url = reverse('daily-measures', args=[2019, 12])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
