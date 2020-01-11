from rest_framework import serializers
from .models import ReservationSeason


class ReservationSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationSeason
        fields = ('season_start',
                  'season_end',
                  'summer_semester_start',
                  'summer_semester_end',
                  'winter_semester_start',
                  'winter_semester_end',
                  'is_current')
