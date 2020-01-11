from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import serializers
from reservation_season.models import ReservationSeason
from reservation_season.serializers import ReservationSeasonSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_season(request):
    if not request.user.is_admin:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        season = ReservationSeason.objects.get(is_current=True)
    except ReservationSeason.DoesNotExist():
        return Response(data={'error': 'Nie znaleziono semestru! Dodaj nowy'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer = ReservationSeasonSerializer(season)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_season(request):
    if not request.user.is_admin:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = ReservationSeasonSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_200_OK)
