from datetime import date

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ReservationSeason(models.Model):
    season_start = models.DateField(null=False)
    season_end = models.DateField(null=False)
    summer_semester_start = models.DateField(null=False)
    summer_semester_end = models.DateField(null=False)
    winter_semester_start = models.DateField(null=False)
    winter_semester_end = models.DateField(null=False)
    is_current = models.BooleanField(default=True)

    def is_in_future(self, demanded_date):
        return (self.season_start <= date.today() <= self.season_end) and (demanded_date >= date.today())


@receiver(post_save, sender=ReservationSeason)
def validate_is_current(sender, instance=None, **kwargs):
    if instance.is_current:
        seasons = ReservationSeason.objects.filter(is_current=True)
        for season in seasons:
            if not season == instance:
                season.is_current = False
                season.save()
