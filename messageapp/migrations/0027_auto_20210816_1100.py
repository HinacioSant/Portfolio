# Generated by Django 3.0.6 on 2021-08-16 14:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messageapp', '0026_auto_20210730_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msa',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 16, 14, 0, 12, 840437, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='r_request',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 16, 14, 0, 12, 840437, tzinfo=utc)),
        ),
    ]
