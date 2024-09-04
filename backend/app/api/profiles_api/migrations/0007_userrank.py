# Generated by Django 5.0.6 on 2024-09-04 07:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0006_profile_daily_profile_email_notification_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('town_rank', models.IntegerField(default=0)),
                ('company_rank', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_rank', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
