# Generated by Django 2.2.8 on 2020-01-07 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200107_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='room_number',
            field=models.TextField(null=True),
        ),
    ]
