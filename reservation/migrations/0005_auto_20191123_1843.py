# Generated by Django 2.2.7 on 2019-11-23 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_auto_20191123_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='semester',
            field=models.CharField(blank=True, choices=[('LETNI', 'Letni'), ('ZIMOWY', 'Zimowy')], default='', max_length=255, null=True),
        ),
    ]
