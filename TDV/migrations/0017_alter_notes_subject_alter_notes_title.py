# Generated by Django 4.0.2 on 2022-09-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TDV', '0016_auto_20211213_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='subject',
            field=models.CharField(blank=True, default='-', max_length=64),
        ),
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(blank=True, default='-', max_length=64),
        ),
    ]