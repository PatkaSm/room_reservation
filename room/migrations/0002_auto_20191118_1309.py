# Generated by Django 2.2.4 on 2019-11-18 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='nuber_of_computers',
            new_name='number_of_computers',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='nuber_of_seats',
            new_name='number_of_seats',
        ),
    ]
