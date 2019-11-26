from datetime import datetime, date
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mysite import variables
from reservation.models import Reservation
from .models import Room
from .serializers import RoomSerializer


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def show_available_rooms(request):
    if request.method == 'POST':
        try:
            data = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
            # Zakładamy, że rezerwacji jednorazowych można dokonywać w czasie 1 października - 31 lipca
            if date(variables.TODAY.year, 10, 1) <= data <= date(variables.TODAY.year, 12, 31):
                year_starts = date(variables.TODAY.year, 10, 1)
                year_finish = date(variables.TODAY.year + 1, 6, 14)

            elif date(variables.TODAY.year, 1, 1) <= data <= date(variables.TODAY.year, 7, 31):
                year_starts = date(variables.TODAY.year - 1, 10, 1)
                year_finish = date(variables.TODAY.year, 7, 31)

            else:
                return Response(
                    data={'errors': 'Nie można rejestrować sali poza rokiem akademickim i sesją poprawkową, '
                                    'ani na przyszłe lata!'},
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except ValueError:
            data = {'error': 'Zły format daty. Prawidłowy format daty to RRRR-MM-DD'}
            return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        # Sprawdzenie czy data rezerwacji jest większa niż dzisiejsza
        if data >= variables.TODAY and year_starts <= data <= year_finish:
            # Lista godzin w których można rezerwować salę
            base_hours = [datetime.strptime('8:00', '%H:%M').time(), datetime.strptime('9:45', '%H:%M').time(),
                          datetime.strptime('11:30', '%H:%M').time(), datetime.strptime('13:15', '%H:%M').time(),
                          datetime.strptime('15:00', '%H:%M').time(), datetime.strptime('16:45', '%H:%M').time(),
                          datetime.strptime('18:30', '%H:%M').time()]
            rooms = Room.objects.all()

            if rooms:
                fulfilled_requirements = []  # lista na sale, które spełniają wymagania użytkownika
                # Słownik zawierający sale, które spełniają wymagania oraz listę godzin w których są dostępne
                # Dane będą występować w formacie
                # final_rooms = {'nazwa_pokoju skrzydło': [     godzina1,
                #                                               godzina2,
                #                                               godzina3...]}
                final_rooms = {}

                for room in rooms:
                    try:
                        # sprawdzamy czy wymagania są spełnione
                        if (room.number_of_computers >= int(request.data['number_of_computers'])
                                and room.number_of_seats >= int(request.data['number_of_seats'])
                                and room.additional_equipment == request.data['additional_equipment']):
                            # jeżeli tak to dodajemy pokój do listy
                            fulfilled_requirements.append(room)
                    except ValueError:
                        # Błąd wyrzucony w przypadku podania liczby w zlym formacie
                        data = {'error': 'Liczba miejsc i komputerów musi być liczbą całkowitą!'}
                        return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

                reservations = Reservation.objects.all()
                try:
                    hour_from = datetime.strptime(request.data['from_hour'], '%H:%M').time()
                    hour_to = datetime.strptime(request.data['to_hour'], '%H:%M').time()
                except ValueError:
                    # Wyjątek rzucony w momencie podania godziny w złym formacie
                    data = {'error': 'Zły format godziny. Prawidłowy format godziny to hh:mm'}
                    return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

                # Tablica w której umieszczone będą godziny które mieszczą się w wymaganiach podanych przez użytkownika
                possible_hours = []
                if hour_from < hour_to:
                    for hour in base_hours:
                        if hour_to >= hour >= hour_from:
                            possible_hours.append(hour)

                for fulfilled_room in fulfilled_requirements:
                    # kopiujemy listę z godzinami mieszczącymi się w wymaganiach użytkownika
                    hours = possible_hours[:]
                    # sprawdzamy teraz w jakich godzinach, pokoje spełniające wymagania są dostępne

                    for reservation in reservations:
                        if datetime.strptime(request.data['date'], '%Y-%m-%d').date() == reservation.date \
                                and fulfilled_room.id == reservation.room.id:
                            # Jeżeli dla danego pokoju istnieje rezerwacja na daną godzinę to jest usuwana ona z listy
                            if reservation.hour in hours:
                                hours.remove(reservation.hour)

                    # Dopisujemy listę godzin dla danego pokoju, do słownika final_rooms
                    final_rooms[str(fulfilled_room.number) + ' ' + str(fulfilled_room.wing)] = hours
                return Response(data=final_rooms, status=status.HTTP_200_OK)

            else:
                # Występuje kiedy w bazie danych nie ma ani jednej sali
                return Response(
                    data={'errors': 'Nie znaleziono sal w bazie danych'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Występuje kiedy rezerwujemy salę w przeszłości
            data = {'error': 'Nie można zarezerwować sali w przeszłości'}
            return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        # Występuje, kiedy metoda jest nieprawidłowa
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
