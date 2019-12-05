from datetime import date
from dateutil import rrule
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import reservation


class ReservationSeason(models.Model):
    season_start = models.DateField(null=False)
    season_end = models.DateField(null=False)
    summer_semester_start = models.DateField(null=False)
    summer_semester_end = models.DateField(null=False)
    winter_semester_start = models.DateField(null=False)
    winter_semester_end = models.DateField(null=False)
    is_current = models.BooleanField(default=True)

    def generate_dates(self, reservation_date, is_every_two_weeks):
        interval = 1
        if is_every_two_weeks:
            interval = 2
        if (self.summer_semester_start <= reservation_date <= self.summer_semester_end
                and self.summer_semester_start <= date.today() <= self.summer_semester_end):
            reservation_dates = list(
                rrule.rrule(rrule.WEEKLY, interval=interval, dtstart=reservation_date, until=self.summer_semester_end))
        elif (self.winter_semester_start <= reservation_date <= self.winter_semester_end
              and self.winter_semester_start <= date.today() <= self.winter_semester_end):
            reservation_dates = list(
                rrule.rrule(rrule.WEEKLY, interval=interval, dtstart=reservation_date, until=self.winter_semester_end))
        else:
            raise ValueError('Nie można rezerwować sal cyklicznie poza aktualnym semestrem')
        return reservation_dates


@receiver(post_save, sender=ReservationSeason)
def validate_is_current(sender, instance=None, **kwargs):
    if instance.is_current:
        seasons = ReservationSeason.objects.filter(is_current=True)
        for season in seasons:
            if not season == instance:
                season.is_current = False
                season.save()
