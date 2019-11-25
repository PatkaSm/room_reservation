from datetime import datetime, timedelta

from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from mysite import settings
from reservation.models import Reservation
from user.models import User
from .models import Room
import json


class RoomTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('create', include('reservation.urls')),
    ]

    def test_add_reservation(self):
        url = reverse('add_reservation')
        data = {'date': datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d'),
                'hour': '8:00',
                'user': '1',
                'room': '1',
                'is_cyclic': 'False',
                'semester': '',
                'is_every_two_weeks': 'False'
                }
        test_room = Room.objects.create(number='127', wing='B2', number_of_seats=120, number_of_computers=0)
        test_user = User.objects.create(email='test@test.test', first_name='Krystyna', last_name='Pawlacz',
                                        password='1234567890')
        test_reservation = Reservation.objects.create(date=datetime.strptime('2019-12-12', '%Y-%m-%d'),
                                                      hour=datetime.strptime('9:45', '%H:%M').time(), room=test_room,
                                                      user=test_user)

        print('\n \n \n =============================TESTY REZERWACJI ====================================\n\n\n')

        print(
            '----------REZULTAT POPRWNEJ JEDNORAZOWEJ REZERWACJI W DOSTĘNYMM TERMINIE W AKTUALNYM SEMESTRZE----------\n')
        response = self.client.post(url, data=data, format='json')
        settings.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count(), 2)
        # ilość rezerwacji w bazie
        count = Reservation.objects.all().count()

        print('\n----------REZERWACJA W ZAJĘTYM JUŻ TEMINIE----------\n')
        data['hour'] = '9:45'
        data['date'] = '2019-12-12'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(Reservation.objects.all().count(), 2)
        # ILOŚĆ REZERWACJI W BAZIE - 2(BEZ ZMIAN)

        print(
            '\n----------REZERWACJA CYKLICZNA CO DWA TYGODNIE W SEMESTRZE LETNIM PODCZAS SEMESTRU LETNIEGO----------\n')
        data['is_cyclic'] = 'True'
        data['is_every_two_weeks'] = 'True'
        data['semester'] = 'LETNI'
        settings.TODAY = datetime.strptime('2020-02-24', '%Y-%m-%d').date()
        data['date'] = '2020-02-24'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count() - count,
                         int(json.loads(response.content)['ilosc']))
        count = Reservation.objects.all().count()

        print('\n----------REZERWACJA CYKLICZNA CO DWA TYGODNIE W SEMESTRZE ZIMOWYM PODCZAS SEMESTRU '
              'ZIMOWEGO----------\n')
        data['is_every_two_weeks'] = 'True'
        data['date'] = '2019-10-01'
        data['semester'] = 'ZIMOWY'
        settings.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count() - count,
                         int(json.loads(response.content)['ilosc']))
        count = Reservation.objects.all().count()

        print('\n----------REZERWACJA SALI W SEMESTRZE LETNIM PODCZAS SEMESTRU ZIMOWEGO----------\n')
        data['is_every_two_weeks'] = 'False'
        data['semester'] = 'LETNI'
        data['date'] = '2020-02-24'
        settings.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        print('\n----------REZERWACJA SALI W SEMESTRZE LETNIM PODCZAS SEMESTRU LETNIEGO----------\n')
        settings.TODAY = datetime.strptime('2020-02-24', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count() - count,
                         int(json.loads(response.content)['ilosc']))

        print('\n----------REZERWACJA SALI W SEMESTRZE ZIMOWYM PODCZAS SEMESTRU LETNIEGO----------\n')
        data['semester'] = 'ZIMOWY'
        settings.TODAY = datetime.strptime('2020-03-24', '%Y-%m-%d').date()
        data['date'] = '2019-12-19'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        count = Reservation.objects.all().count()

        print('\n----------REZERWACJA SALI W SEMESTRZE ZIMOWYM PODCZAS SEMESTRU ZIMOWEGO----------\n')
        settings.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        data['date'] = '2019-10-01'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count() - count,
                         int(json.loads(response.content)['ilosc']))

        print('\n----------FORMAT DANYCH----------\n')
        data['hour'] = 'ósma'
        data['date'] = '2020:12:22'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        print('\n--------------------------------------------------------------------------------------\n')
