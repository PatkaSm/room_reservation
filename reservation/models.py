from django.db import models
from django.conf import settings

from room.models import Room


class Reservation(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    hour = models.TimeField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_cyclic = models.BooleanField(default=False)
    is_every_two_weeks = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.date) + ' ' + str(self.room)

    @staticmethod
    def create_reservation(reservation_date, reservation_hour, user, room, is_cyclic, is_every_two_weeks):
        pass



