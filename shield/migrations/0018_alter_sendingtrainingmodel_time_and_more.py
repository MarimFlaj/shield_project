# Generated by Django 5.0.3 on 2024-04-15 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shield', '0017_alter_sendingurlsmodel_send_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendingtrainingmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 15, 7, 50, 28, 905688, tzinfo=datetime.timezone.utc), verbose_name='Sending Time'),
        ),
        migrations.AlterField(
            model_name='sendingurlsmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 15, 7, 50, 28, 905688, tzinfo=datetime.timezone.utc), verbose_name='Sending Time'),
        ),
    ]
