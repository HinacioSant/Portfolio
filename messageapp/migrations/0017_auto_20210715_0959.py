# Generated by Django 3.0.6 on 2021-07-15 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageapp', '0016_auto_20210714_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msa',
            name='time',
            field=models.CharField(max_length=20),
        ),
    ]