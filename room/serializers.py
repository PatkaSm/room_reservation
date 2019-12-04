from datetime import date

from rest_framework import serializers

from reservation_season.models import ReservationSeason
from .models import Room
from .models import Equipment


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'wing', 'number_of_seats', 'number_of_computers', 'additional_equipment')


class DemandingSerializer(serializers.Serializer):
    reservation_date = serializers.DateField()
    reservation_hour_from = serializers.TimeField()
    reservation_hour_to = serializers.TimeField()
    number_of_seats = serializers.IntegerField()
    number_of_computers = serializers.IntegerField()
    additional_equipment = serializers.ChoiceField(choices=Equipment, default='BRAK')

    def validate(self, data):
        if data['reservation_hour_from'] > data['reservation_hour_to']:
            raise serializers.ValidationError("Zła kolejność godzin!")
        if data['reservation_date'] < date.today():
            raise serializers.ValidationError("Nie można rezerwować sali w przeszłości")
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
