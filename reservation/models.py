from django.db import models
from django.conf import settings

from room.models import Room

SEMESTER = [('LETNI', 'Letni'), ('ZIMOWY', 'Zimowy')]


class Reservation(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    hour = models.TimeField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_cyclic = models.BooleanField(default=False)
    semester = models.CharField(max_length=255, choices=SEMESTER, default='ZIMOWY')
    is_every_two_week = models.BooleanField(default=False, null=True, blank=True)

    def __set__(self):
        return str(self.date) + ' ' + self.room
