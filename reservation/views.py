from datetime import datetime, timedelta, date
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mysite import variables
from reservation_season.models import ReservationSeason
from .models import Reservation, AvailabilityException
from .serializer import ReservationSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservation_create(request):
    serializer = ReservationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        current_season = ReservationSeason.objects.get(is_current=True)
    except ReservationSeason.DoesNotExist:
        data = {'error': 'Sezon rezerwacji nie został ustanowiony przez administratora'}
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    if date.today() < current_season.season_start or date.today() > current_season.season_end:
        return Response(data={'data': "Nie możesz rezerwować sali podczas trwania wakacji"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    reservation_date = serializer.validated_data.get('date')
    reservation_hour = serializer.validated_data.get('hour')
    is_cyclic = serializer.validated_data.get("is_cyclic", False)
    is_every_two_weeks = serializer.validated_data.get('is_every_two_weeks', False)
    room = serializer.validated_data.get('room')

    if reservation_date > current_season.season_end or reservation_date < current_season.season_start:
        return Response(data={'errors': "Próbujesz zarezerwować salę na inny rok akademicki"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if not is_cyclic:
        if room.is_available(date=reservation_date, hour=reservation_hour):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'errors': 'Sala nie jest wtedy dostępna'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        generated_dates = current_season.generate_dates(reservation_date, is_every_two_weeks)
    except ValueError as error:
        return Response(data={'errors': str(error)},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    data = Reservation.create_cyclic_reservation(reservation_hour, request.user, room, generated_dates)
    Reservation.objects.bulk_create(data['reservations'])
    data['reservations'] = 'Pomyślnie zarejestrowano to końca semestru z wyjątkiem: '
    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reservation_delete(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    operation = reservation.delete()
    data = {}
    if operation:
        data["success"] = "Delete successfully"
    else:
        data["failure"] = "Delete failed"
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)
