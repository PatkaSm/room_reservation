from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'hour', 'date', 'user', 'room', 'is_cyclic', 'semester', 'is_every_two_week')
