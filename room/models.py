from datetime import time

from django.db import models

Equipment = [('BRAK', 'Brak'), ('STEROWNIKI', 'Sterowniki'), ('PRACOWNIA_FIZYCZNA', 'Pracownia fizyczna')]


class Room(models.Model):
    number = models.IntegerField()
    wing = models.CharField(max_length=2)
    number_of_seats = models.IntegerField()
    number_of_computers = models.IntegerField()
    additional_equipment = models.CharField(max_length=50, choices=Equipment, default='BRAK')

    def __str__(self):
        return str(self.number) + ' ' + self.wing

    def is_available(self, date, hour):
        return not reservation.models.Reservation.objects.filter(room=self, date=date, hour=hour).exists()

    @staticmethod
    def show_available(reservation_date, reservation_hour_from, reservation_hour_to,
                       number_of_seats, number_of_computers, additional_equipment):

        base_hours = [time(8, 0), time(9, 45), time(11, 30), time(13, 15), time(15, 0), time(16, 45), time(18, 30)]
        hours_that_fulfill = []  # lista na godziny które pasują użytkownikowi
        for hour in base_hours:
            if reservation_hour_from <= hour <= reservation_hour_to:
                hours_that_fulfill.append(hour)

        # Słownik zawierający sale, które spełniają wymagania oraz listę godzin w których są dostępne
        # Dane będą występować w formacie
        # final_rooms = {'nazwa_pokoju skrzydło': [     godzina1,
        #                                               godzina2,
        #                                               godzina3...]}
        rooms_that_fulfill = []  # lista na sale, które spełniają wymagania użytkownika
        final_dict = {}
        room_list = Room.objects.all()
        for room in room_list:
            if (room.number_of_computers >= number_of_computers and room.number_of_seats >= number_of_seats
                    and room.additional_equipment == additional_equipment):
                rooms_that_fulfill.append(room)

        for room in rooms_that_fulfill:
            room_hours = hours_that_fulfill[:]
            reservation_list = reservation.models.Reservation.objects.filter(room=room, date=reservation_date)
            for reserv in reservation_list:
                if reserv.hour in room_hours:
                    room_hours.remove(reserv.hour)
            if not len(room_hours) == 0:
                final_dict[str(room.number) + ' ' + str(room.wing)] = room_hours
        return final_dict


import reservation.models
