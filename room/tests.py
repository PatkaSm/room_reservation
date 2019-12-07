import unittest

from room.models import Room
from reservation.models import Reservation
from datetime import date, time, datetime
from freezegun import freeze_time


# MOCK OBJECTS FOR ROOM#


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('\n ============== JEDNOSTKOWE TESTY WYŚWIETLANIA DOSTĘPNYCH SAL ============== \n')
        test_room_1 = Room(id=1, number=126, wing='B2', number_of_seats=125, number_of_computers=0)
        test_room_2 = Room(id=2, number=127, wing='B2', number_of_seats=125, number_of_computers=0)
        test_room_3 = Room(id=3, number=128, wing='B2', number_of_seats=125, number_of_computers=0)
        test_room_4 = Room(id=4, number=129, wing='B2', number_of_seats=125, number_of_computers=0)
        test_room_5 = Room(id=5, number=130, wing='B2', number_of_seats=125, number_of_computers=0)

        cls.room_list = [test_room_1, test_room_2, test_room_3, test_room_4, test_room_5]

        test_reservation_1 = Reservation(date=date(2019, 10, 3), hour=time(8, 0), user_id=1, room=test_room_1,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_2 = Reservation(date=date(2019, 10, 3), hour=time(9, 45), user_id=1, room=test_room_2,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_3 = Reservation(date=date(2019, 10, 3), hour=time(11, 30), user_id=1, room=test_room_3,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_4 = Reservation(date=date(2019, 10, 3), hour=time(16, 45), user_id=1, room=test_room_4,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_5 = Reservation(date=date(2019, 10, 3), hour=time(15, 0), user_id=1, room=test_room_5,
                                         is_cyclic=False, is_every_two_weeks=False)

        cls.reservation_list = [test_reservation_1, test_reservation_2, test_reservation_3, test_reservation_4,
                                test_reservation_5]

        test_reservation_6 = Reservation(date=date(2019, 10, 9), hour=time(8, 0), user_id=1, room=test_room_2,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_7 = Reservation(date=date(2019, 10, 9), hour=time(9, 45), user_id=1, room=test_room_2,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_8 = Reservation(date=date(2019, 10, 9), hour=time(11, 30), user_id=1, room=test_room_2,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_9 = Reservation(date=date(2019, 10, 9), hour=time(13, 15), user_id=1, room=test_room_2,
                                         is_cyclic=False, is_every_two_weeks=False)
        test_reservation_10 = Reservation(date=date(2019, 10, 9), hour=time(15, 0), user_id=1, room=test_room_2,
                                          is_cyclic=False, is_every_two_weeks=False)
        test_reservation_11 = Reservation(date=date(2019, 10, 9), hour=time(16, 45), user_id=1, room=test_room_2,
                                          is_cyclic=False, is_every_two_weeks=False)
        test_reservation_12 = Reservation(date=date(2019, 10, 9), hour=time(18, 30), user_id=1, room=test_room_2,
                                          is_cyclic=False, is_every_two_weeks=False)

        cls.busy_reservation_list = [test_reservation_6, test_reservation_7, test_reservation_8, test_reservation_9,
                                     test_reservation_10, test_reservation_11, test_reservation_12]

    # WYŚWIETLANIE SŁOWNIKA GDZIE 5 SAL JEST ZAWSZE WOLNYCH
    @freeze_time('2019-10-01')
    def test_with_no_reservations_blocking(self):
        print(" \n------------------------------------ TEST NR 1 ------------------------------------\n ")
        test_list_1 = Room.show_available(date(2019, 10, 7), time(8, 0), time(20, 0),
                                          0, 0, 'BRAK', self.room_list, self.reservation_list)

        self.assertEqual(len(test_list_1), 5, msg='Nieprawidłowa ilość zwróconych sal')
        self.assertEqual(type(test_list_1), dict, msg='Nie zgadza się typ zwróconych danych w teście nr 1')
        self.assertEqual(type(test_list_1['126 B2']), list,
                         msg='Format godzin dla sali 126 B2 nie zgadza się w teście nr 1')
        for sala in test_list_1.keys():
            self.assertEqual(len(test_list_1[sala]), 7,
                             msg="Sala w której nie zgadza się to: {} w teście nr 1".format(sala))

    # WYŚWIETLANIE SŁOWNIKA GDZIE JEDNA SALA NIE JEST WOLNA W OGÓLE
    @freeze_time('2019-10-01')
    def test_where_room_is_not_avaliable_at_all(self):
        print(" \n------------------------------------ TEST NR 2 ------------------------------------ \n")
        test_list_2 = Room.show_available(date(2019, 10, 9), time(8, 0), time(20, 0), 10, 0, 'BRAK', self.room_list,
                                          self.busy_reservation_list)
        self.assertEqual(type(test_list_2), dict, msg='Typ zwróconych danych nie zgadza się w teście nr 2')
        self.assertEqual(type(test_list_2['126 B2']), list,
                         msg='Format godzin dla sali 126 B2 nie zgadza się w teście nr 2')
        self.assertEqual(len(test_list_2), 4, msg="Ilość sal się nie zgadza w teście nr 2")

    # WYŚWIETLANIE SŁOWNIKA GDZIE W KAŻDEJ SALI JEST ZAJĘTA KTÓRAŚ Z GODZIN
    @freeze_time('2019-10-01')
    def test_where_room_is_avaliable_but_not_all_day(self):
        print(" \n------------------------------------ TEST NR 3 ------------------------------------\n ")
        room_is_available_not_all_day = []
        test_list_3 = Room.show_available(date(2019, 10, 3), time(8, 0), time(20, 0), 10, 0, 'BRAK', self.room_list,
                                          self.reservation_list)
        # sprawdzamy sale mające mniej niż 7 dostępnych godzin rezerwacji danego dnia i dodajemy je do listy
        for sala in test_list_3.keys():
            if len(test_list_3[sala]) < 7:
                room_is_available_not_all_day.append(sala)
        self.assertEqual(type(test_list_3), dict, msg='Typ zwróconych danych nie zgadza się w teście nr 3')
        self.assertEqual(type(test_list_3['126 B2']), list,
                         msg='Format godzin dla sali 126 B2 nie zgadza się w teście nr 3')
        self.assertEqual(len(room_is_available_not_all_day), 5,
                         msg='Któraś z sal jest wolna przez cały dzień w teście nr 3')

    @freeze_time('2019-10-01')
    def test_where_user_set_night_hours(self):
        print(" \n ------------------------------------ TEST NR 4 ------------------------------------ \n ")
        self.assertRaises(ValueError,
                          Room.show_available, date(2019, 10, 3), time(1, 0), time(7, 0), 10, 0, 'BRAK', self.room_list,
                          self.reservation_list)


"""from datetime import datetime, timedelta

from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from mysite import variables
from reservation.models import Reservation
from room import views
from user.models import User
from .models import Room
import json


class RoomTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('rooms/show_available/rooms/', include('room.urls')),
    ]

    def test_showing_available_rooms(self):
        url = reverse('show_available_rooms')
        data = {'date': datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d'),
                'number_of_seats': '10',
                'number_of_computers': '10',
                'additional_equipment': 'BRAK',
                'from_hour': '8:00',
                'to_hour': '18:30'
                }
        variables.TODAY = datetime.now().date()
        test_room = Room.objects.create(number='126', wing='B2', number_of_seats=15, number_of_computers=15)
        Room.objects.create(number='127', wing='B2', number_of_seats=15, number_of_computers=0)
        test_user = User.objects.create(email='test@test.test', first_name='Andrzej', last_name='Testowy',
                                        password='1234567890')
        Reservation.objects.create(date=datetime.now() + timedelta(days=1),
                                   hour=datetime.strptime('8:00', '%H:%M').time(), room=test_room, user=test_user)

        print('\n \n \n ==================================TESTY DOSTĘPNYCH SAL'
              ' =========================================\n\n\n ')

        print('\n----------WYSWIETLANIE DOSTĘPNYCH GODZIN GDY DANE SIĘ ZGADZAJĄ----------\n')
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'126 B2': ['09:45:00', '11:30:00', '13:15:00', '15:00:00', '16:45:00', '18:30:00']})

        print('\n----------WYSWIETLANIE DOSTĘPNYCH GODZIN GDY DANE SIĘ ZGADZAJĄ, DLA DWÓCH SAL----------\n')
        data['number_of_seats'] = '5'
        data['number_of_computers'] = '0'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'126 B2': ['09:45:00',
                                     '11:30:00',
                                     '13:15:00',
                                     '15:00:00',
                                     '16:45:00',
                                     '18:30:00'],
                          '127 B2': ['08:00:00',
                                     '09:45:00',
                                     '11:30:00',
                                     '13:15:00',
                                     '15:00:00',
                                     '16:45:00',
                                     '18:30:00']}
                         )

        print('\n----------SPRAWDZANIE CZY FORMAT GODZINY JEST ODPOWIEDNI----------\n')
        data['from_hour'] = '8;00'
        data['to_hour'] = '18.30'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(json.loads(response.content),
                         {'error': 'Zły format godziny. Prawidłowy format godziny to hh:mm'})
        data['from_hour'] = '8:00'
        data['to_hour'] = '18:30'
        data['date'] = datetime.strftime(datetime.now() - timedelta(days=1), '%Y-%m-%d')

        print('\n----------SPRAWDZANIE CZY DATA REZERWACJI JEST W PRZYSZŁOŚCI----------\n')
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(json.loads(response.content),
                         {'error': 'Nie można zarezerwować sali w przeszłości'})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        data['date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%Y:%m:%d')

        print('\n----------SPRAWDZANIE CZY FORMAT DATY JEST PRAWIDŁOWY----------\n')
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(json.loads(response.content),
                         {'error': 'Zły format daty. Prawidłowy format daty to RRRR-MM-DD'})
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data['number_of_seats'] = 'dziesięć'
        data['number_of_computers'] = 'dziesięć'
        data['date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d')

        print('\n----------SPRAWDZANIE CZY WYMAGANIA LICZBOWE SĄ PODANE POPRAWNIE----------\n')
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(json.loads(response.content),
                         {'error': 'Liczba miejsc i komputerów musi być liczbą całkowitą!'})
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        print('\n----------SPRAWDZANIE CZY REZERWACJA JEST MOŻLIWA POZA ROKIEM AKADEMICKIM----------\n')
        data['date'] = '2020-08-08'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(json.loads(response.content),
                         {'errors': 'Nie można rejestrować sali poza rokiem akademickim i sesją poprawkową, '
                                    'ani na przyszłe lata!'})

        print('\n----------SPRAWDZANIE CZY REZERWACJA JEST MOŻLIWA NA INNY ROK AKADEMICKI----------\n')
        data['date'] = '2021-10-11'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(json.loads(response.content),
                         {'errors': 'Nie można rejestrować sali poza rokiem akademickim i sesją poprawkową, '
                                    'ani na przyszłe lata!'})
        print('\n----------------------------------------------------------------------\n')"""
