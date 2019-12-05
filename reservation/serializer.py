from datetime import time

from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'hour', 'date', 'room', 'is_cyclic', 'is_every_two_weeks')

    def validate(self, data):
        base_hours = [time(8, 0), time(9, 45), time(11, 30), time(13, 15), time(15, 0), time(16, 45), time(18, 30)]
        if data['hour'] not in base_hours:
            raise serializers.ValidationError('Podano złą godzinę rezerwacji')
        return data
