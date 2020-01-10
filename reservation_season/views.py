from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import serializers
from reservation_season.models import ReservationSeason


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_season(request):
    if not request.user.is_admin:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        season = ReservationSeason.objects.get(is_current=True)
    except ReservationSeason.DoesNotExist():
        return Response(data={'error': 'Nie znaleziono semestru! Dodaj nowy'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    response_data = {
        'season_start': season.season_start,
        'season_end': season.season_end,
        'summer_semester_start': season.summer_semester_start,
        'summer_semester_end': season.summer_semester_end,
        'winter_semester_start': season.winter_semester_start,
        'winter_semester_end': season.winter_semester_end,
        'is_current': season.is_current
    }
    return Response(data=response_data, status=status.HTTP_200_OK)
