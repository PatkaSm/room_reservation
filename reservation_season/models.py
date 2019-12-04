from datetime import date

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class ReservationSeason(models.Model):
    season_start = models.DateField(null=False, default=timezone.now())
    season_end = models.DateField(null=False, default=timezone.now())
    summer_semester_start = models.DateField(null=False, default=timezone.now())
    summer_semester_end = models.DateField(null=False, default=timezone.now())
    winter_semester_starts = models.DateField(null=False, default=timezone.now())
    summer_semester_starts = models.DateField(null=False, default=timezone.now())
    is_current = models.BooleanField(default=True)


@receiver(post_save, sender=ReservationSeason)
def validate_is_current(sender, instance=None, **kwargs):
    if instance.is_current:
        seasons = ReservationSeason.objects.filter(is_current=True)
        for season in seasons:
            if not season == instance:
                season.is_current = False
                season.save()
