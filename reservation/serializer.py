from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'url', 'hour', 'date', 'user', 'room', 'is_cyclic')
