# Generated by Django 3.0.6 on 2021-10-14 13:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messageapp', '0031_auto_20211007_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msa',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 14, 13, 56, 20, 203917, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='r_request',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 14, 13, 56, 20, 204916, tzinfo=utc)),
        ),
    ]