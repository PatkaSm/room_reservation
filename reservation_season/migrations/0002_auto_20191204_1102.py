# Generated by Django 2.2.7 on 2019-12-04 10:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_season', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationseason',
            name='season_end',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324698, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reservationseason',
            name='season_start',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324659, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reservationseason',
            name='summer_semester_end',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324726, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reservationseason',
            name='summer_semester_start',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324714, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reservationseason',
            name='summer_semester_starts',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324748, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reservationseason',
            name='winter_semester_starts',
            field=models.DateField(default=datetime.datetime(2019, 12, 4, 10, 2, 57, 324737, tzinfo=utc)),
        ),
    ]
