from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class MeasureQuerySet(models.QuerySet):
    def from_year(self, year):
        return self.filter(date__year=year)

    def from_month(self, month):
        return self.filter(date__month=month)

    def get_monthly_averages_of_year(self, year):
        return self.filter(date__year=year) \
            .values_list('date__month') \
            .order_by('date__month') \
            .annotate(weight_avg=Avg('weight'))

    def get_annual_averages(self):
        return self.values_list('date__year') \
            .order_by('date__year') \
            .annotate(weight_avg=Avg('weight'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.IntegerField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Measure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField()

    measures = MeasureQuerySet.as_manager()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date} - {self.weight} kg'
