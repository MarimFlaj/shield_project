# Generated by Django 4.2.2 on 2024-03-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shield', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Department',
            field=models.CharField(default=1, max_length=30, verbose_name='Department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='Status',
            field=models.CharField(default=1, max_length=30, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gander',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default=1, max_length=10, verbose_name='Gander'),
            preserve_default=False,
        ),
    ]
