from calendar import month
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from .models import Reservation
from .serializer import ReservationSerializer


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@api_view(['POST'])
def reservation_create(request):
    reservations = Reservation.objects.all()
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            if not request.data["is_cyclic"]:
                for resevation in reservations:
                    if resevation.date == datetime.strptime(request.data['date'], '%Y-%m-%d').date() \
                            and resevation.hour == datetime.strptime(request.data['hour'], '%H:%M').time():
                        return Response(data={'error': 'Sala jest zarezerowana w tym terminie!'},
                                        status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                if request.data["semester"] == "LETNI":
                    last_day = '2020-06-14'
                    first_reservation_date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
                    end_of_semester = datetime.strptime(
                        last_day, '%m %d').date().replace(year=datetime.strptime(request.data['date'], '%Y-%m-%d'
                                                                                 ).date().year)
                    while first_reservation_date < end_of_semester:
                        serializer.save()
                else:
                    last_day = '2020-01-26'
                    end_of_semester = datetime.strptime(
                        last_day, '%m %d').date().replace(year=datetime.strptime(request.data['date'], '%Y-%m-%d'
                                                                                 ).date().year)
                    first_reservation_date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
                    while first_reservation_date < end_of_semester:
                        pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def reservation_delete(request, pk):
    try:
        resevation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = resevation.delete()
        data = {}
        if operation:
            data["success"] = "delete succesful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@api_view(['GET'])
def reservation_detail(request, pk):
    try:
        resevation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReservationSerializer(resevation)
        return Response(serializer.data)
