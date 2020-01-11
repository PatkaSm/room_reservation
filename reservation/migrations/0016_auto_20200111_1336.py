# Generated by Django 2.2.8 on 2020-01-11 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_auto_20200111_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='room.Room'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
