import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from measures.models import Measure


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@gmail.com', 'pass')
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

    def test_from_year_method(self):
        measures = Measure.measures.from_year(2019)
        self.assertEquals(measures.count(), 2)

    def test_from_month_method(self):
        measures = Measure.measures.from_month(12)
        self.assertEquals(measures.count(), 2)

    def test_get_monthly_averages_of_year(self):
        monthly_avgs = Measure.measures.get_monthly_averages_of_year(2019)
        self.assertEquals(monthly_avgs.count(), 1)
        self.assertTupleEqual(monthly_avgs[0], (12, 92.5))

    def test_get_annual_averages(self):
        annual_avgs = Measure.measures.get_annual_averages()
        self.assertEquals(annual_avgs.count(), 2)
        self.assertTupleEqual(annual_avgs[1], (2019, 92.5))
