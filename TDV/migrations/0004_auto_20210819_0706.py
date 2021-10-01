# Generated by Django 3.0.6 on 2021-08-19 10:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TDV', '0003_auto_20210817_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 19, 10, 6, 6, 97250, tzinfo=utc)),
        ),
    ]