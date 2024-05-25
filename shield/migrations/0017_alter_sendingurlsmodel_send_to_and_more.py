# Generated by Django 5.0.3 on 2024-04-05 17:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shield', '0016_alter_sendingurlsmodel_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendingurlsmodel',
            name='send_to',
            field=models.CharField(choices=[('user', 'user'), ('department', 'department')], max_length=10, verbose_name='Send To'),
        ),
        migrations.AlterField(
            model_name='sendingurlsmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 5, 17, 6, 57, 39987), verbose_name='Sending Time'),
        ),
        migrations.CreateModel(
            name='SendingTrainingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2024, 4, 5, 17, 6, 57, 39987), verbose_name='Sending Time')),
                ('send_to', models.CharField(choices=[('user', 'user'), ('department', 'department')], max_length=10, verbose_name='Send To')),
                ('Department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shield.departmentmodel', verbose_name='Department')),
                ('Train_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shield.trainingpackage', verbose_name='Training Package')),
                ('U_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Sending TrainingPackage ',
                'verbose_name_plural': 'Sending TrainingPackages',
                'db_table': 'SendingTrainingPackage',
            },
        ),
    ]
