# Generated by Django 2.2.8 on 2020-01-11 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0010_auto_20200111_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='room',
            new_name='reservation_room',
        ),
    ]
