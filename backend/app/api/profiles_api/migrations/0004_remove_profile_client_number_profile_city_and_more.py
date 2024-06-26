# Generated by Django 5.0.6 on 2024-05-29 15:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0003_remove_profile_id_alter_profile_profile_picture_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='client_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Sofia', max_length=30),
        ),
        migrations.CreateModel(
            name='ClientNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_number', models.CharField(max_length=15, unique=True)),
                ('users', models.ManyToManyField(related_name='client_numbers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaterMeter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meter_number', models.CharField(max_length=20)),
                ('client_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_meters', to='profiles_api.clientnumber')),
            ],
        ),
        migrations.CreateModel(
            name='WaterMeterReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_meter_readings', to=settings.AUTH_USER_MODEL)),
                ('water_meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_meter_readings', to='profiles_api.watermeter')),
            ],
        ),
    ]
