from django.db import models

Equipment = [('BRAK','Brak'),('STEROWNIKI', 'Sterowniki'), ('PRACOWNIA_FIZYCZNA', 'Pracownia fizyczna')]


class Room(models.Model):
    number = models.IntegerField()
    wing = models.CharField(max_length=2)
    number_of_seats = models.IntegerField()
    number_of_computers = models.IntegerField()
    additional_equipment = models.CharField(max_length=50, choices=Equipment, default='BRAK')

    def __str__(self):
        return str(self.number) + ' ' + self.wing
