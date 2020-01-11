from datetime import date

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

from reservation_season.models import ReservationSeason
from user.models import User


class ReservationSeasonCreatingTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(ReservationSeasonCreatingTests, cls).setUpClass()
        print('\n  ==============  TESTY TWORZENIA ROKU AKADEMICKIEGO ============== \n ')

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_admin = User.objects.create_superuser(email='test@test.test', first_name='Andrzej',
                                                       last_name='Testowy',
                                                       password='1234567890')
        cls.test_user = User.objects.create_user(email='test@test2.test', first_name='Andrzej',
                                                 last_name='Testowy',
                                                 password='1234567890')

        cls.data = {'season_start': '2019-10-01',
                    'season_end': '2020-07-31',
                    'summer_semester_start': '2020-02-01',
                    'summer_semester_end': '2019-06-30',
                    'winter_semester_start': '2019-10-01',
                    'winter_semester_end': '2019-01-31'
                    }
        cls.old_seasaon = ReservationSeason.objects.create(season_start=date(2019, 9, 23),
                                                           season_end=date(2020, 7, 31),
                                                           summer_semester_start=date(2020, 2, 14),
                                                           summer_semester_end=date(2020, 6, 14),
                                                           winter_semester_start=date(2019, 10, 1),
                                                           winter_semester_end=date(2020, 1, 25), is_current=True)
        cls.get_season_url = reverse('get_season')
        cls.new_season_url = reverse('new_season')

    @freeze_time('2019-10-01')
    def test_integration_reservation_1(self):
        print('\n----------POBIERANIE DANYCH O ROKU AKADEMICKIM JAKO ADMIN----------\n')
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(self.get_season_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg='Zły response status code w teście integracyjnym nr 1')

    @freeze_time('2019-10-01')
    def test_integration_reservation_2(self):
        print('\n----------POBIERANIE DANYCH O ROKU AKADEMICKIM JAKO NIE ADMIN----------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.get_season_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg='Zły response status code w teście integracyjnym nr 2')

    # TODO TESTY DOKOŃCZYĆ
    @freeze_time('2019-10-01')
    def test_integration_reservation_3(self):
        print('\n----------USTALANIE NOWEGO ROKU AKADEMICKIEGO JAKO ADMIN---------\n')
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post(self.new_season_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg='Zły response status code w teście integracyjnym nr 3')
        self.assertEqual(ReservationSeason.objects.all().count(), 2, msg='Zła ilość lat akademickich')
        self.assertEqual(ReservationSeason.objects.filter(is_current=True).count(), 1,
                         msg='Zła ilość aktywmych lat akademickich')

    @freeze_time('2019-10-01')
    def test_integration_reservation_4(self):
        print('\n----------USTALANIE NOWEGO ROKU AKADEMICKIEGO JAKO NIEADMIN---------\n')
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.new_season_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg='Zły response status code w teście integracyjnym nr 4')
        self.assertEqual(ReservationSeason.objects.all().count(), 1, msg='Zła ilość lat akademickich')
