# Generated by Django 5.0.3 on 2024-05-21 03:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shield', '0023_alter_sendingtrainingmodel_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendingtrainingmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 21, 3, 5, 57, 508958), verbose_name='Sending Time'),
        ),
        migrations.AlterField(
            model_name='sendingurlsmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 21, 3, 5, 57, 508958), verbose_name='Sending Time'),
        ),
    ]
