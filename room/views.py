from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from reservation.models import Reservation
from .models import Room
from .serializers import RoomSerializer


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# TODO
"""
1)Zabezpieczenie przed dodaniem rezerwacji w przeszłości
2) Dodanie godzinowych widełek czasowych

"""
@api_view(['POST'])
@permission_classes([AllowAny])
def show_available_rooms(request):
    possible_hours = [datetime.strptime('8:00', '%H:%M').time(), datetime.strptime('9:45', '%H:%M').time(),
                      datetime.strptime('11:30', '%H:%M').time(), datetime.strptime('13:15', '%H:%M').time(),
                      datetime.strptime('15:00', '%H:%M').time(), datetime.strptime('16:45', '%H:%M').time(),
                      datetime.strptime('18:30', '%H:%M').time()]
    rooms = Room.objects.all()
    fulfilled_requirements = []  # rooms that fulfil user's requirements
    final_rooms = {}
    for room in rooms:
        if (room.number_of_computers >= int(request.data['number_of_computers'])
                and room.number_of_seats >= int(request.data['number_of_seats'])
                and room.additional_equipment == request.data['additional_equipment']):
            fulfilled_requirements.append(room)
    reservations = Reservation.objects.all()
    for fulfilled_room in fulfilled_requirements:
        hours = possible_hours[:]
        for reservation in reservations:
            if datetime.strptime(request.data['date'], '%Y-%m-%d').date() == reservation.date and fulfilled_room.id == reservation.room.id:
                hours.remove(reservation.hour)
        final_rooms[str(fulfilled_room.number) + ' ' + str(fulfilled_room.wing)] = hours
    return JsonResponse(final_rooms, status=200)