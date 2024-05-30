from datetime import datetime
from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os
from PIL import Image


def get_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('profile_pics', filename)


def validate_image(image):
    max_size_kb = 5 * 1024 * 1024
    if image.size > max_size_kb:
        raise ValidationError(f"Image file too large ( > 5MB )")

    ext = os.path.splitext(image.name)[1]
    valid_extensions = ['.png', '.jpeg', '.jpg']
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}. Use: .png, .jpeg, .jpg")


class Profile(models.Model):

    FIRST_NAME_MAX_LENGTH = 30
    LATEST_NAME_MAX_LENGTH = 30
    PHONE_NUMBER_MAX_LENGTH = 15
    MAX_CITY_LENGTH = 30

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='profile',
                                blank=False,
                                null=False)

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH,
                                  blank=True,
                                  null=True)

    last_name = models.CharField(max_length=LATEST_NAME_MAX_LENGTH,
                                 blank=True,
                                 null=True)

    city = models.CharField(max_length=MAX_CITY_LENGTH,
                            default='Sofia')

    email = models.EmailField()

    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH,
                                    blank=True,
                                    null=True)

    profile_picture = models.ImageField(upload_to=get_unique_filename,
                                        validators=[validate_image])

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.profile_picture:
            super().save(*args, **kwargs)

            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

        else:
            super().save(*args, **kwargs)


class ClientNumber(models.Model):
    CLIENT_NUMBER_MAX_LENGTH = 15

    client_number = models.CharField(max_length=CLIENT_NUMBER_MAX_LENGTH,
                                     unique=True)

    users = models.ManyToManyField(User, related_name='client_numbers')

    def __str__(self):
        return self.client_number


class WaterMeter(models.Model):
    WATER_METER_NUMBER_MAX_LENGTH = 20

    client_number = models.ForeignKey(ClientNumber,
                                      on_delete=models.CASCADE,
                                      related_name='water_meters')

    meter_number = models.CharField(max_length=WATER_METER_NUMBER_MAX_LENGTH)

    def __str__(self):
        return f"Water Meter {self.meter_number} for {self.client_number}"

    def calculate_average_monthly_consumption(self):
        readings = self.water_meter_readings.order_by('-date')[:2]
        if len(readings) < 2:
            return "Not enough data to calculate average monthly consumption."

        first_reading = readings[1]
        latest_reading = readings[0]

        value_diff = latest_reading.value - first_reading.value
        days_diff = (latest_reading.date - first_reading.date).days

        if days_diff == 0:
            return "Invalid data: consecutive readings have the same date."

        average_daily_consumption = value_diff / days_diff
        average_daily_consumption = round(average_daily_consumption, 3)
        average_monthly_consumption = average_daily_consumption * 30
        average_monthly_consumption = round(average_monthly_consumption, 3)

        if days_diff < 30:
            return {
                "approximate": True,
                "average_monthly_consumption": average_monthly_consumption
            }
        else:
            return {
                "approximate": False,
                "average_monthly_consumption": average_monthly_consumption
            }


class WaterMeterReading(models.Model):
    VALUE_MAX_LENGTH = 10

    water_meter = models.ForeignKey(WaterMeter,
                                    on_delete=models.CASCADE,
                                    related_name='water_meter_readings')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='water_meter_readings')

    value = models.IntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reading {self.value} for {self.water_meter} by {self.user}"

    def save(self, *args, **kwargs):
        if self.pk:  # If the object is not new (already exists)
            last_reading = WaterMeterReading.objects.filter(
                water_meter=self.water_meter,
                date__lt=self.date
            ).order_by('-date').first()

            if last_reading and (self.value < last_reading.value or self.value > last_reading.value + 1000):
                raise ValidationError(
                    "The value should not be less than the previous reading or greater "
                    "than 1000 to the last saved reading.")

        super().save(*args, **kwargs)
