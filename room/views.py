from datetime import date
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import DemandingSerializer
from reservation_season.models import ReservationSeason
from .models import Room
from .serializers import RoomSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def show_available_rooms(request):
    try:
        current_season = ReservationSeason.objects.get(is_current=True)
    except ReservationSeason.DoesNotExist:
        data = {'error': 'Sezon rezerwacji nie został ustanowiony przez administratora'}
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = DemandingSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    reservation_date = serializer.validated_data.get('reservation_date')
    hour_from = serializer.validated_data.get('reservation_hour_from')
    hour_to = serializer.validated_data.get('reservation_hour_to')
    number_of_computers = serializer.validated_data.get('number_of_computers')
    number_of_seats = serializer.validated_data.get('number_of_seats')
    additional_equipment = serializer.validated_data.get('additional_equipment')

    if date.today() < current_season.season_start or date.today() > current_season.season_end:
        return Response(data={'data': "Nie możesz rezerwować sali podczas trwania wakacji"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if reservation_date > current_season.season_end or reservation_date < current_season.season_start:
        return Response(data={'errors': "Próbujesz zarezerwować salę na inny rok akademicki"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response(data=Room.show_available(reservation_date, hour_from, hour_to, number_of_seats, number_of_computers,
                                             additional_equipment), status=status.HTTP_200_OK)
