from datetime import datetime
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
        except ValueError:
            data = {'error': 'Zły format daty. Prawidłowy format daty to RRRR-MM-DD'}
            return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        if data >= datetime.now().date():
            base_hours = [datetime.strptime('8:00', '%H:%M').time(), datetime.strptime('9:45', '%H:%M').time(),
                          datetime.strptime('11:30', '%H:%M').time(), datetime.strptime('13:15', '%H:%M').time(),
                          datetime.strptime('15:00', '%H:%M').time(), datetime.strptime('16:45', '%H:%M').time(),
                          datetime.strptime('18:30', '%H:%M').time()]
            rooms = Room.objects.all()
            if rooms:
                fulfilled_requirements = []  # rooms that fulfil user's requirements
                final_rooms = {}
                for room in rooms:
                    try:
                        if (room.number_of_computers >= int(request.data['number_of_computers'])
                                and room.number_of_seats >= int(request.data['number_of_seats'])
                                and room.additional_equipment == request.data['additional_equipment']):
                            fulfilled_requirements.append(room)
                    except ValueError:
                        data = {'error': 'Liczba miejsc i komputerów musi być liczbą całkowitą!'}
                        return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                reservations = Reservation.objects.all()
                try:
                    hour_from = datetime.strptime(request.data['from_hour'], '%H:%M').time()
                    hour_to = datetime.strptime(request.data['to_hour'], '%H:%M').time()
                except ValueError:
                    data = {'error': 'Zły format godziny. Prawidłowy format godziny to hh:mm'}
                    return Response(data=data, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                possible_hours = []
                if hour_from < hour_to:
                    for hour in base_hours:
                        if hour_to >= hour >= hour_from:
                            possible_hours.append(hour)
                for fulfilled_room in fulfilled_requirements:
                    hours = possible_hours[:]
                    for reservation in reservations:
                        if datetime.strptime(request.data['date'], '%Y-%m-%d').date() == reservation.date \
                                and fulfilled_room.id == reservation.room.id:
                            if reservation.hour in hours:
                                hours.remove(reservation.hour)
                    final_rooms[str(fulfilled_room.number) + ' ' + str(fulfilled_room.wing)] = hours
                return Response(data=final_rooms, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'errors': 'Nie znaleziono sal w bazie danych'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = {'error': 'Nie można zarezerwować sali w przeszłości'}
            return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
