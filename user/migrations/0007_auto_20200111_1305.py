# Generated by Django 2.2.8 on 2020-01-11 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200107_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True),
        ),
    ]
