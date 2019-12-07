"""from datetime import datetime, timedelta, date

from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from mysite import variables
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
        data = {'date': datetime.strftime(variables.TODAY + timedelta(days=1), '%Y-%m-%d'),
                'hour': '8:00',
                'user': '1',
                'room': '1',
                'is_cyclic': 'False',
                'semester': '',
                'is_every_two_weeks': 'False'
                }
        variables.TODAY = datetime.now().date()
        test_room = Room.objects.create(number='127', wing='B2', number_of_seats=120, number_of_computers=0)
        test_user = User.objects.create(email='test@test.test', first_name='Krystyna', last_name='Pawlacz',
                                        password='1234567890')
        test_reservation = Reservation.objects.create(date=datetime.strptime('2019-12-12', '%Y-%m-%d'),
                                                      hour=datetime.strptime('9:45', '%H:%M').time(), room=test_room,
                                                      user=test_user)

        print(
            '\n \n \n ============================TESTY DODAWANIA REZERWACJI ===================================\n\n\n')

        print(
            '---------REZULTAT POPRAWNEJ JEDNORAZOWEJ REZERWACJI W DOSTĘNYMM TERMINIE W AKTUALNYM SEMESTRZE---------\n')
        variables.TODAY = datetime.strptime('2019-10-01', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
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
        variables.TODAY = datetime.strptime('2020-02-24', '%Y-%m-%d').date()
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
        variables.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
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
        variables.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        print('\n----------REZERWACJA SALI W SEMESTRZE LETNIM PODCZAS SEMESTRU LETNIEGO----------\n')
        variables.TODAY = datetime.strptime('2020-02-24', '%Y-%m-%d').date()
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count() - count,
                         int(json.loads(response.content)['ilosc']))

        print('\n----------REZERWACJA SALI W SEMESTRZE ZIMOWYM PODCZAS SEMESTRU LETNIEGO----------\n')
        data['semester'] = 'ZIMOWY'
        variables.TODAY = datetime.strptime('2020-03-24', '%Y-%m-%d').date()
        data['date'] = '2019-12-19'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        count = Reservation.objects.all().count()

        print('\n----------REZERWACJA SALI W SEMESTRZE ZIMOWYM PODCZAS SEMESTRU ZIMOWEGO----------\n')
        variables.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
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

        print('\n----------REZERWACJA SALI NA INNY ROK AKADEMICKI----------\n')
        data['hour'] = '8:00'
        variables.TODAY = datetime.strptime('2019-12-12', '%Y-%m-%d').date()
        data['date'] = '2020-12-22'
        response = self.client.post(url, data=data, format='json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        print('\n--------------------------------------------------------------------------------------\n')

    def test_reservation_delete(self):
        print(
            '\n \n \n ============================TESTY USUWANIA REZERWACJI ===================================\n\n\n')
        variables.TODAY = date(2019, 10, 1)
        test_room = Room.objects.create(number='125', wing='B3', number_of_seats=110, number_of_computers=15)
        test_user = User.objects.create(email='test@test.test', first_name='Krystyna', last_name='Pawlacz',
                                        password='1234567890')
        test_reservation = Reservation.objects.create(date=datetime.strptime('2019-12-12', '%Y-%m-%d'),
                                                      hour=datetime.strptime('9:45', '%H:%M').time(), room=test_room,
                                                      user=test_user)

        print('\n----------CZY REZERWACJA JEST USUWANA, GDY NIE ISTNIEJE----------\n')
        url = reverse('reservation_delete', args=[22])
        response = self.client.delete(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Reservation.objects.all().count(), 1)
        print(response.content)

        print('\n----------CZY REZERWACJA JEST USUWANA, GDY ISTNIEJE----------\n')
        url = reverse('reservation_delete', args=[test_reservation.id])
        response = self.client.delete(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.all().count(), 0)
        self.assertEqual(json.loads(response.content), {'success': 'Delete successfully'})
        print(json.loads(response.content))

    def test_reservation_detail(self):
        print(
            '\n \n \n ==========================TESTY WYŚWIETLANIA REZERWACJI ================================\n\n\n')
        variables.TODAY = date(2019, 10, 1)
        test_room = Room.objects.create(number='125', wing='B3', number_of_seats=110, number_of_computers=15)
        test_user = User.objects.create(email='test@test.test', first_name='Krystyna', last_name='Pawlacz',
                                        password='1234567899')
        test_reservation = Reservation.objects.create(date=datetime.strptime('2019-12-12', '%Y-%m-%d'),
                                                      hour=datetime.strptime('9:45', '%H:%M').time(), room=test_room,
                                                      user=test_user)
        url = reverse('reservation_detail', args=[test_reservation.id])
        print('\n----------CZYT REZERWACJA JEST WYŚWIETLANA POPRAWNIE GDY ISTNIEJE----------\n')
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(json.loads(response.content),
                         {'id': 1, 'hour': '09:45:00', 'date': '2019-12-12', 'user': 1, 'room': 1,
                          'is_cyclic': False, 'semester': '', 'is_every_two_weeks': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print('\n----------CZYT REZERWACJA JEST WYŚWIETLANA POPRAWNIE GDY NIE ISTNIEJE----------\n')
        url = reverse('reservation_detail', args=[2])
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)"""
