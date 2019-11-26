from datetime import datetime, timedelta, date

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mysite import variables
from .models import Reservation
from .serializer import ReservationSerializer


@api_view(['POST'])
def reservation_create(request):
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            # Zakładamy, że rezerwacji można dokonywać w czasie 1 października - 31 lipca
            if date(variables.TODAY.year, 10, 1) <= serializer.validated_data['date'] \
                    <= date(variables.TODAY.year, 12, 31):
                year_starts = date(variables.TODAY.year, 10, 1)
                year_finish = date(variables.TODAY.year + 1, 6, 14)

            elif date(variables.TODAY.year, 1, 1) <= serializer.validated_data['date'] \
                    <= date(variables.TODAY.year, 7, 31):
                year_starts = date(variables.TODAY.year - 1, 10, 1)
                year_finish = date(variables.TODAY.year, 7, 31)

            else:
                return Response(data={'errors': 'Nie można rejestrować sali poza rokiem akademickim'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not (year_starts <= serializer.validated_data['date'] <= year_finish):
                return Response(data={'errors': 'Nie można rejestrować sali na inny rok akademicki niż aktualny'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not serializer.validated_data["is_cyclic"]:
                if not is_available(room=serializer.validated_data['room'], date=serializer.validated_data['date'],
                                    hour=serializer.validated_data['hour']):
                    return Response(data={'error': 'Sala jest zarezerwowana w tym terminie!'},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:  # Jeżeli rezerwacja jest cykliczna, sprawdzamy w jakim semestrze.
                if serializer.validated_data["semester"] == "LETNI":
                    first_day = datetime.strptime('2020-02-24', '%Y-%m-%d')
                    last_day = '2020-06-14'
                    first_reservation_date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
                    end_of_semester = datetime.strptime(
                        last_day, '%Y-%m-%d').date().replace(year=datetime.strptime(request.data['date'], '%Y-%m-%d'
                                                                                    ).date().year)

                    # Sprawdzamy czy data dzisiejsza jest większa niż tydzień przed rozpoczęciem semestru
                    if (variables.TODAY > (
                            first_day - timedelta(weeks=1)).date()) and variables.TODAY <= end_of_semester:
                        data = {'success': 'Pomyślnie zarezerwowano do końca semestru letniego', 'exceptions': [],
                                'ilosc': '0'}
                        # Rezerwacje tworzymy co tydzień, lub co dwa od podanej daty początkowej do końca semestru
                        licznik = 0  # LICZNIK STWORZONYCH REZERWACJI

                        while first_reservation_date <= end_of_semester:
                            if is_available(room=serializer.validated_data['room'], date=first_reservation_date,
                                            hour=serializer.validated_data['hour']):
                                Reservation.objects.create(date=first_reservation_date,
                                                           hour=serializer.validated_data['hour'],
                                                           user=serializer.validated_data['user'],
                                                           room=serializer.validated_data['room'],
                                                           is_cyclic=serializer.validated_data['is_cyclic'],
                                                           semester=serializer.validated_data['semester'])
                                licznik += 1

                            else:
                                # jeżeli podczas procesu rezerwacji cyklicznej algorytm napotka na swojej drodze
                                # rezerwację w tym samym czasie to doda jej datę do listy ['exceptions']
                                data[
                                    'success'] = 'Pomyślnie zarezerwowano do końca semestru letniego, z wyjątkami,' \
                                                 ' skontaktuj się z dziekanatem'
                                data['exceptions'].append(datetime.strftime(first_reservation_date, '%Y-%m-%d'))

                                # Instrukcja sprawdzająca czy rezerwujemy co tydzień czy co dwa.
                            if serializer.validated_data['is_every_two_weeks']:
                                first_reservation_date = first_reservation_date + timedelta(weeks=2)
                            else:
                                first_reservation_date = first_reservation_date + timedelta(weeks=1)

                        data['ilosc'] = str(licznik)
                        return Response(data=data,
                                        status=status.HTTP_201_CREATED)

                    else:
                        return Response(
                            data={'errors': 'Jest semestr zimowy. Za wcześnie na rezerwacje w semestrze letnim'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

                elif serializer.validated_data['semester'] == 'ZIMOWY':
                    first_day = datetime.strptime('2019-10-01', '%Y-%m-%d')
                    last_day = '2020-01-26'
                    first_reservation_date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()

                    # Jeśli rezerwacja jest w styczniu lub przed 24 lutego, to nie dodajemy kolejnego roku do
                    # końca semestru
                    if first_reservation_date.month < 2 or (
                            first_reservation_date.month == 2 and first_reservation_date.day <= 24):
                        end_of_semester = datetime.strptime(
                            last_day, '%Y-%m-%d').date().replace(year=datetime.strptime(request.data['date'], '%Y-%m-%d'
                                                                                        ).date().year)
                    else:  # jeśli początek rezerwacji jest od października do końca grudnia musimy dodać
                        # 1 do roku bieżącego
                        end_of_semester = datetime.strptime(
                            last_day, '%Y-%m-%d').date().replace(year=datetime.strptime(request.data['date'], '%Y-%m-%d'
                                                                                        ).date().year + 1)
                    if (first_day - timedelta(weeks=1)).date() < variables.TODAY <= end_of_semester:
                        data = {'success': 'Pomyślnie zarezerwowano do końca semestru zimowego', 'exceptions': [],
                                'ilosc': '0'}
                        licznik = 0  # LICZNIK STWORZONYCH REZERWACJI
                        while first_reservation_date <= end_of_semester:
                            if is_available(room=serializer.validated_data['room'], date=first_reservation_date,
                                            hour=serializer.validated_data['hour']):
                                Reservation.objects.create(date=first_reservation_date,
                                                           hour=serializer.validated_data['hour'],
                                                           user=serializer.validated_data['user'],
                                                           room=serializer.validated_data['room'],
                                                           is_cyclic=serializer.validated_data['is_cyclic'],
                                                           semester=serializer.validated_data['semester'])
                                licznik += 1
                            else:
                                data['success'] = 'Pomyślnie zarezerwowano do końca semestru zimowego, z wyjątkami,' \
                                                  ' skontaktuj się z dziekanatem'
                                data['exceptions'].append(datetime.strftime(first_reservation_date, '%Y-%m-%d'))
                            if serializer.validated_data['is_every_two_weeks']:
                                first_reservation_date = first_reservation_date + timedelta(weeks=2)
                            else:
                                first_reservation_date = first_reservation_date + timedelta(weeks=1)
                        data['ilosc'] = str(licznik)
                        return Response(data=data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response(
                            data={'errors': 'Aktualnie trwa semestr letni, więc Nie możesz '
                                            'zarezerwować sali na semestr zimowy'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    return Response(data={'error': 'Metoda niedozwolona'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Funkcja sprawdzająca czy sala jest dostępna w danym terminie
def is_available(room, date, hour):
    reservations = Reservation.objects.all()
    for reservation in reservations:
        if date == reservation.date and room.id == reservation.room.id and hour == reservation.hour:
            return False
    return True


@api_view(['DELETE'])
def reservation_delete(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = reservation.delete()
        data = {}
        if operation:
            data["success"] = "Delete successfully"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
