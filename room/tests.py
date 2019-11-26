from datetime import datetime, timedelta

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
        print('\n----------------------------------------------------------------------\n')


