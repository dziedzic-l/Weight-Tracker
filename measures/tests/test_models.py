from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from measures.models import Measure, MeasureQuerySet


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@gmail.com', 'pass')
        Measure.measures.create(
            user=self.user,
            weight=93,
            date=date(2019, 12, 30)
        )
        Measure.measures.create(
            user=self.user,
            weight=93,
            date=date(2018, 11, 2)
        )
        Measure.measures.create(
            user=self.user,
            weight=92,
            date=date(2019, 12, 29)
        )

    def test_from_year_method(self):
        measures = Measure.measures.from_year(2019)
        self.assertEquals(measures.count(), 2)
        self.assertIsInstance(measures, MeasureQuerySet)

    def test_from_month_method(self):
        measures = Measure.measures.from_month(12)
        self.assertEquals(measures.count(), 2)
        self.assertIsInstance(measures, MeasureQuerySet)

    def test_get_monthly_averages_of_year(self):
        monthly_avgs = Measure.measures.get_monthly_averages_of_year(2019)
        measure_data_from_december = {
            'date__month': 12,
            'weight_avg': 92.5
        }
        self.assertEquals(monthly_avgs.count(), 1)
        self.assertDictEqual(monthly_avgs[0], measure_data_from_december)
        self.assertIsInstance(monthly_avgs, MeasureQuerySet)

    def test_get_annual_averages(self):
        annual_avgs = Measure.measures.get_annual_averages()
        measure_data_from_2019 = {
            'date__year': 2019,
            'weight_avg': 92.5
        }
        self.assertEquals(annual_avgs.count(), 2)
        self.assertDictEqual(annual_avgs[1], measure_data_from_2019)
        self.assertIsInstance(annual_avgs, MeasureQuerySet)
