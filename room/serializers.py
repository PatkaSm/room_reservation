from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'wing', 'number_of_seats', 'number_of_computers', 'additional_equipment')

