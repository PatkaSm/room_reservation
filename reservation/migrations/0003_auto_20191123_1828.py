# Generated by Django 2.2.7 on 2019-11-23 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20191122_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='is_every_two_week',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
