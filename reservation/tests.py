import json
from datetime import datetime, timedelta, date, time
from django.urls import reverse, path, include
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, force_authenticate, APIClient, APIRequestFactory
from reservation.models import Reservation
from reservation_season.models import ReservationSeason
from user.models import User
from .models import Room


class ReservationIntegrationTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('create', include('reservation.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super(ReservationIntegrationTests, cls).setUpClass()
        print('\n  ============== INTEGRACYJNE TESTY REZERWACJI ============== \n ')

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_room = Room.objects.create(number='126', wing='B2', number_of_seats=15, number_of_computers=15)
        cls.test_room_2 = Room.objects.create(number='127', wing='B2', number_of_seats=15, number_of_computers=0)
        cls.test_user = User.objects.create(email='test@test.test', first_name='Andrzej', last_name='Testowy',
                                            password='1234567890')
        cls.test_user2 = User.objects.create(email='test@test2.test', first_name='Andrzej', last_name='Testowy',
                                            password='1234567890')
        cls.test_admin = User.objects.create_superuser(email='test@test3.test', first_name='Andrzej', last_name='Testowy',
                                             password='1234567890')

        test_reservation1 = Reservation.objects.create(date='2019-10-10',
                                                       hour=datetime.strptime('8:00', '%H:%M').time(),
                                                       room=cls.test_room, user=cls.test_user)
        test_reservation2 = Reservation.objects.create(date='2019-10-17',
                                                       hour=datetime.strptime('8:00', '%H:%M').time(),
                                                       room=cls.test_room, user=cls.test_user)

        cls.data = {'date': '2019-10-03',
                    'hour': '8:00',
                    'is_cyclic': False,
                    'is_every_two_weeks': False,
                    'room': '1',
                    }

        cls.current_season = ReservationSeason.objects.create(season_start=date(2019, 9, 23),
                                                              season_end=date(2020, 7, 31),
                                                              summer_semester_start=date(2020, 2, 14),
                                                              summer_semester_end=date(2020, 6, 14),
                                                              winter_semester_start=date(2019, 10, 1),
                                                              winter_semester_end=date(2020, 1, 25), is_current=True)
        cls.add_reservation_url = reverse('add_reservation')
        cls.my_reservations_url = reverse('my_reservations')
        cls.reservation_detail_url = reverse('reservation_detail', kwargs={'pk': 1})
        cls.reservation_delete_url = reverse('reservation_delete', kwargs={'pk': 1})
        cls.all_reservations_url = reverse('all_reservations')

    @freeze_time('2019-10-01')
    def test_integration_reservation_1(self):
        print('\n----------REZERWACJA JEDNORAZOWA W AKTUALNYM ROKU AKADEMICKIM----------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg='Zły response status code w teście integracyjnym nr 1')

    @freeze_time('2019-10-01')
    def test_integration_reservation_2(self):
        print('\n----------REZERWACJA JEDNORAZOWA POZA AKTUALNYM ROKIEM AKADEMICKIM----------\n')
        self.data['date'] = '2020-10-22'
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 2')

    @freeze_time('2019-10-01')
    def test_integration_reservation_3(self):
        print('\n----------REZERWACJA JEDNORAZOWA W TRAKCIE WAKACJI----------\n')
        self.data['date'] = '2020-08-22'
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 3')

    @freeze_time('2019-10-01')
    def test_integration_reservation_4(self):
        print('\n----------REZERWACJA JEDNORAZOWA W ZAJĘTYM TERMINIE---------\n')
        self.data['date'] = '2020-10-10'
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 4')

    @freeze_time('2019-10-01')
    def test_integration_reservation_5(self):
        print('\n----------REZERWACJA CYKLICZNA W AKTUALNYM ROKU AKADEMICKIM---------\n')
        self.data['date'] = '2019-10-09'
        self.data['is_cyclic'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg='Zły response status code w teście integracyjnym nr 5')
        self.assertEqual(Reservation.objects.all().count() - 2, 16,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr 5')

    @freeze_time('2019-10-01')
    def test_integration_reservation_6(self):
        print('\n----------REZERWACJA CYKLICZNA GDY NIE WSZYSKIE TERMINY SĄ WOLNE---------\n')
        self.data['date'] = '2019-10-03'
        self.data['is_cyclic'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg='Zły response status code w teście integracyjnym nr 6')
        self.assertEqual(Reservation.objects.all().count() - 2, 15,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr nr 6')

    @freeze_time('2019-10-01')
    def test_integration_reservation_7(self):
        print('\n----------REZERWACJA CYKLICZNA W AKTUALNYM ROKU AKADEMICKIM CO DWA TYGONIE---------\n')
        self.data['date'] = '2019-10-04'
        self.data['is_cyclic'] = True
        self.data['is_every_two_weeks'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg='Zły response status code w teście integracyjnym nr 7')
        self.assertEqual(Reservation.objects.all().count() - 2, 9,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr nr 7')

    @freeze_time('2019-10-01')
    def test_integration_reservation_8(self):
        print('\n----------REZERWACJA CYKLICZNA POZA AKTULNYM ROKIEM AKADEMICKIM--------\n')
        self.data['date'] = '2020-10-09'
        self.data['is_cyclic'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 8')
        self.assertEqual(Reservation.objects.all().count() - 2, 0,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr 8')

    @freeze_time('2019-10-01')
    def test_integration_reservation_9(self):
        print('\n----------REZERWACJA CYKLICZNA W SEMESTRZE ZIMOWYM NA SEMESTR LETNI--------\n')
        self.data['date'] = '2020-03-09'
        self.data['is_cyclic'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 9')
        self.assertEqual(Reservation.objects.all().count() - 2, 0,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr 9')

    @freeze_time('2020-03-09')
    def test_integration_reservation_10(self):
        print('\n----------REZERWACJA CYKLICZNA W SEMESTRZE LETNIM NA SEMESTR ZIMOWY--------\n')
        self.data['date'] = '2019-10-09'
        self.data['is_cyclic'] = True
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.add_reservation_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE,
                         msg='Zły response status code w teście integracyjnym nr 10')
        self.assertEqual(Reservation.objects.all().count() - 2, 0,
                         msg='Zła liczba sworzonych rezerwacji w teście integracyjnym nr 10')

    @freeze_time('2020-03-09')
    def test_integration_reservation_11(self):
        print('\n----------ZWRACANIE LISTY REZERWACJI UŻYTKOWNIKA--------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.my_reservations_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         [{'id': 1, 'room_number': 126, 'room_wing': 'B2', 'date': '2019-10-10', 'hour': '08:00'},
                          {'id': 2, 'room_number': 126, 'room_wing': 'B2', 'date': '2019-10-17', 'hour': '08:00'}])

    @freeze_time('2020-03-09')
    def test_integration_reservation_12(self):
        print('\n----------ZWRACANIE SZCZEGÓŁÓW REZERWACJI--------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.reservation_detail_url, data={}, format='json')
        self.assertEqual(json.loads(response.content), {'id': 1, 'hour': '08:00:00', 'date': '2019-10-10',
                                                        'room': 1, 'is_cyclic': False, 'is_every_two_weeks': False
                                                        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time('2020-03-09')
    def test_integration_reservation_13(self):
        print('\n----------ZWRACANIE SZCZEGÓŁÓW REZERWACJI BEZ UPRAWNIEN--------\n')
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.get(self.reservation_detail_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time('2020-03-09')
    def test_integration_reservation_14(self):
        print('\n----------USUWANIE REZERWACJI--------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(self.reservation_delete_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.all().count(), 1)

    @freeze_time('2020-03-09')
    def test_integration_reservation_14(self):
        print('\n----------USUWANIE REZERWACJI BEZ UPRAWNIEN--------\n')
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.delete(self.reservation_delete_url, data={}, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Reservation.objects.all().count(), 2)

    @freeze_time('2020-03-09')
    def test_integration_reservation_15(self):
        print('\n----------ZWRACANIE WSZYSTKICH REZERWACJI PRZEZ ADMINA--------\n')
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(self.all_reservations_url, data={}, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)



