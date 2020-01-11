import unittest
from room.models import Room
from reservation.models import Reservation
from datetime import date, time, datetime
from freezegun import freeze_time
from datetime import datetime, timedelta
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from reservation_season.models import ReservationSeason
from reservation.models import Reservation
from room import views
from user.models import User
from .models import Room
import json


# MOCK OBJECTS FOR ROOM#


class RoomUnitTests(unittest.TestCase):
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
    def test_unit_room_1(self):
        print(" \n------------------------- TEST, GDY 5 SAL JEST WOLNYCH NA CAŁY DZIEŃ -------------------------\n ")
        test_list_1 = Room.show_available(date(2019, 10, 7), time(8, 0), time(20, 0),
                                          0, 0, 'BRAK', self.room_list, self.reservation_list)

        self.assertEqual(len(test_list_1), 5, msg='Nieprawidłowa ilość zwróconych sal')
        self.assertEqual(type(test_list_1), list, msg='Nie zgadza się typ zwróconych danych w teście nr 1')

    # WYŚWIETLANIE SŁOWNIKA GDZIE JEDNA SALA NIE JEST WOLNA W OGÓLE
    @freeze_time('2019-10-01')
    def test_unit_room_2(self):
        print(" \n------------------------- TEST GDY JEDNA SALA NIE JEST WOLNA W OGÓLE ------------------------- \n")
        test_list_2 = Room.show_available(date(2019, 10, 9), time(8, 0), time(20, 0), 10, 0, 'BRAK', self.room_list,
                                          self.busy_reservation_list)
        self.assertEqual(type(test_list_2), list, msg='Typ zwróconych danych nie zgadza się w teście nr 2')
        self.assertEqual(len(test_list_2), 4, msg="Ilość sal się nie zgadza w teście nr 2")

    # WYŚWIETLANIE SŁOWNIKA GDZIE W KAŻDEJ SALI JEST ZAJĘTA KTÓRAŚ Z GODZIN
    @freeze_time('2019-10-01')
    def test_unit_room_3(self):
        print(" \n---------------------- TEST GDY W KAŻDEJ SALI JEST ZAJĘTA KTÓRAŚ Z GODZIN ----------------------\n ")
        test_list_3 = Room.show_available(date(2019, 10, 3), time(8, 0), time(20, 0), 10, 0, 'BRAK', self.room_list,
                                          self.reservation_list)
        self.assertEqual(type(test_list_3), list, msg='Typ zwróconych danych nie zgadza się w teście nr 3')

    @freeze_time('2019-10-01')
    def test_unit_room_4(self):
        print(" \n ------------------------ TEST GDY PODANA JEST ZŁA KOLEJNOŚĆ GODZIN ------------------------ \n ")
        self.assertRaises(ValueError,
                          Room.show_available, date(2019, 10, 3), time(1, 0), time(7, 0), 10, 0, 'BRAK', self.room_list,
                          self.reservation_list)


# Integration tests

class RoomIntegrationTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('rooms/show_available/rooms/', include('room.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super(RoomIntegrationTests, cls).setUpClass()
        print('\n  ============== INTEGRACYJNE TESTY DOSTĘPNYCH SAL ============== \n ')

    @classmethod
    def setUpTestData(cls):
        cls.test_room = Room.objects.create(number='126', wing='B2', number_of_seats=15, number_of_computers=15)
        cls.test_room_2 = Room.objects.create(number='127', wing='B2', number_of_seats=15, number_of_computers=0)
        cls.test_user = User.objects.create(email='test@test.test', first_name='Andrzej', last_name='Testowy',
                                            password='1234567890')
        cls.test_reservation = Reservation.objects.create(date=datetime.now() + timedelta(days=1),
                                                          hour=datetime.strptime('8:00', '%H:%M').time(),
                                                          room=cls.test_room, user=cls.test_user)
        cls.data = {'reservation_date': datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d'),
                    'number_of_seats': '10',
                    'number_of_computers': '10',
                    'additional_equipment': 'Brak',
                    'reservation_hour_from': '8:00',
                    'reservation_hour_to': '18:30'
                    }
        cls.current_season = ReservationSeason.objects.create(season_start=date(2019, 10, 1),
                                                              season_end=date(2020, 7, 31),
                                                              summer_semester_start=date(2019, 2, 14),
                                                              summer_semester_end=date(2020, 6, 14),
                                                              winter_semester_start=date(2019, 10, 1),
                                                              winter_semester_end=date(2020, 1, 25), is_current=True)
        cls.url = reverse('show_available_rooms')

    @freeze_time('2019-10-01')
    def test_integration_room_1(self):
        print('\n----------WYSWIETLANIE DOSTĘPNYCH GODZIN GDY DANE SIĘ ZGADZAJĄ----------\n')
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg='Zły response status code w teście integracyjnym nr 1')

    @freeze_time('2019-10-01')
    def test_integration_room_2(self):
        print('\n----------WYSWIETLANIE DOSTĘPNYCH GODZIN GDY DANE SIĘ ZGADZAJĄ, DLA DWÓCH SAL----------\n')
        self.data['number_of_seats'] = '5'
        self.data['number_of_computers'] = '0'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg='Zły response status code w teście integracyjnym nr 2')

    @freeze_time('2019-10-01')
    def test_integration_room_3(self):
        print('\n----------SPRAWDZANIE CZY FORMAT GODZINY JEST ODPOWIEDNI----------\n')
        self.data['reservation_hour_from'] = '8;00'
        self.data['reservation_hour_to'] = '18.30'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(json.loads(response.content),
                         {'reservation_hour_from': [
                             'Błędny format czasu. Użyj jednego z dostępnych formatów: hh:mm[:ss[.uuuuuu]]'],
                             'reservation_hour_to': [
                                 'Błędny format czasu. Użyj jednego z dostępnych formatów: hh:mm[:ss[.uuuuuu]]']},
                         msg='Zła treść response body w teście nr 3')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 3')

    @freeze_time('2019-10-10')
    def test_integration_room_4(self):
        print('\n----------SPRAWDZANIE CZY DATA REZERWACJI JEST W PRZYSZŁOŚCI----------\n')
        self.data['reservation_hour_from'] = '8:00'
        self.data['reservation_hour_to'] = '18:30'
        self.data['reservation_date'] = '2019-10-01'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(json.loads(response.content),
                         {'non_field_errors': ['Nie można rezerwować sali w przeszłości']},
                         msg='Zła treść response body w teście nr 4')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 4')

    @freeze_time('2019-10-01')
    def test_integration_room_5(self):
        print('\n----------SPRAWDZANIE CZY FORMAT DATY JEST PRAWIDŁOWY----------\n')
        self.data['reservation_date'] = '2019/10/1'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(json.loads(response.content),
                         {'reservation_date': ['Data ma zły format. Użyj jednego z tych formatów: YYYY-MM-DD.']},
                         msg='Zła treść response body w teście nr 5')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 5')

    @freeze_time('2019-10-01')
    def test_integration_room_6(self):
        print('\n----------SPRAWDZANIE CZY WYMAGANIA LICZBOWE SĄ PODANE POPRAWNIE----------\n')
        self.data['number_of_seats'] = 'dziesięć'
        self.data['number_of_computers'] = 'dziesięć'
        self.data['reservation_date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d')
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(json.loads(response.content), {'number_of_seats': ['Wymagana poprawna liczba całkowita.'],
                                                        'number_of_computers': ['Wymagana poprawna liczba całkowita.']},
                         msg='Zła treść response body w teście nr 6')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 6')
        self.data['number_of_seats'] = '10'
        self.data['number_of_computers'] = '10'

    @freeze_time('2019-10-01')
    def test_integration_room_7(self):
        print('\n----------SPRAWDZANIE CZY REZERWACJA JEST MOŻLIWA POZA ROKIEM AKADEMICKIM----------\n')
        self.data['reservation_date'] = '2020-08-08'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 7')
        self.assertEqual(json.loads(response.content), {'errors': 'Próbujesz zarezerwować salę na inny rok akademicki'},
                         msg='Zła treść response body w teście nr 7')

    @freeze_time('2019-10-01')
    def test_integration_room_8(self):
        print('\n----------SPRAWDZANIE CZY REZERWACJA JEST MOŻLIWA NA INNY ROK AKADEMICKI----------\n')
        self.data['reservation_date'] = '2021-10-11'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 8')
        self.assertEqual(json.loads(response.content), {'errors': 'Próbujesz zarezerwować salę na inny rok akademicki'},
                         msg='Zła treść response body w teście nr 8')
        print('\n----------------------------------------------------------------------\n')
