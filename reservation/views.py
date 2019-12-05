from datetime import datetime, timedelta, date
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mysite import variables
from reservation_season.models import ReservationSeason
from .models import Reservation
from .serializer import ReservationSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservation_create(request):
    serializer = ReservationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        # Zakładamy, że rezerwacji można dokonywać w czasie 1 października - 31 lipca

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
        if not room.is_available(date=reservation_date, hour=reservation_hour):
            return Response(data={'error': 'Sala jest zarezerwowana w tym terminie!'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    try:
        generated_dates = current_season.generate_dates(reservation_date, is_every_two_weeks)
    except ValueError as error:
        return Response(data={'errors': str(error)},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    reservation_list = []
    exception_list = []
    print(generated_dates)
    for generated_date in generated_dates:
        if room.is_available(generated_date, reservation_hour):
            reservation_list.append(
                Reservation(date=generated_date, hour=reservation_hour, user=request.user, room=room, is_cyclic=True,
                            is_every_two_weeks=False))
        else:
            exception_list.append(datetime.strftime(generated_date, '%Y-%m-%d'))
    Reservation.objects.bulk_create(reservation_list)
    data = {'success': 'Pomyślnie zarezerwowano do końca semestru, z wyjątkiem:', 'exceptions': exception_list,
            'ilosc': str(len(reservation_list))}

    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
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
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)
