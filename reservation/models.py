from datetime import datetime
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

    # Metoda tworząca jednorazową rezerwację
    @staticmethod
    def create_disposable_reservation(reservation_date, reservation_hour, user, room):
        if not room.is_available(date=reservation_date, hour=reservation_hour):
            raise AvailabilityException(message='Sala nie jest wtedy dostępna!',
                                        errors={
                                            '{} {}'.format(room.number, room.wing): 'Sala nie jest wtedy dostępna!'})
        return Reservation.objects.create(date=reservation_date, hour=reservation_hour, user=user, room=room,
                                          is_cyclic=False, is_every_two_weeks=False)

    # Metoda tworząca cykliczną rezerwację
    @staticmethod
    def create_cyclic_reservation(reservation_hour, user, room, generated_dates):
        reservation_list = []
        exception_list = []
        for generated_date in generated_dates:
            if room.is_available(generated_date, reservation_hour):
                reservation_list.append(
                    Reservation(date=generated_date, hour=reservation_hour, user=user, room=room,
                                is_cyclic=True,
                                is_every_two_weeks=False))
            else:
                exception_list.append(datetime.strftime(generated_date, '%Y-%m-%d'))
        Reservation.objects.bulk_create(reservation_list)
        data = {'success': 'Pomyślnie zarezerwowano do końca semestru, z wyjątkiem:', 'exceptions': exception_list,
                'ilosc': str(len(reservation_list))}
        return data


# Deklaracja wyjątku rzucanego podczas sprawdzania czy możemy wykonać jednorazową rezerwację
class AvailabilityException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
