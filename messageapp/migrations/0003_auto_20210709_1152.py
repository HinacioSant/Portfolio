# Generated by Django 3.0.6 on 2021-07-09 14:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messageapp', '0002_auto_20210709_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msa',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 9, 11, 52, 47, 32436)),
        ),
        migrations.AlterField(
            model_name='msa',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usermsa', to=settings.AUTH_USER_MODEL),
        ),
    ]
