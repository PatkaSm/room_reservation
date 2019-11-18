from django.shortcuts import render
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from room.models import Room
from room.serializers import RoomSerializer
from .models import Reservation
from .serializer import ReservationSerializer


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
