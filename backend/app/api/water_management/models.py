from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from api.profiles_api.models import get_unique_filename


class WaterCompany(models.Model):
    MAX_COMPANY_NAME_LENGTH = 30
    PHONE_NUMBER_MAX_LENGTH = 15

    name = models.CharField(max_length=MAX_COMPANY_NAME_LENGTH,
                            blank=False,
                            null=False)

    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH,
                                    blank=True,
                                    null=True)

    email = models.EmailField()

    def __str__(self):
        return self.name


class ClientNumber(models.Model):
    CLIENT_NUMBER_MAX_LENGTH = 15

    users = models.ManyToManyField(User, related_name='client_numbers')

    water_company = models.ForeignKey(WaterCompany,
                                      on_delete=models.CASCADE,
                                      related_name='client_numbers')

    client_number = models.CharField(max_length=CLIENT_NUMBER_MAX_LENGTH,
                                     unique=True)

    def __str__(self):
        return self.client_number


class PropertyTypes(models.Model):
    TYPE_MAX_LENGTH = 30

    type = models.CharField(max_length=TYPE_MAX_LENGTH)
    image = models.ImageField(upload_to=get_unique_filename)

    def __str__(self):
        return self.type


class RoomTypes(models.Model):
    class RoomType(models.TextChoices):
        KITCHEN = 'KITCHEN', 'Kitchen'
        BATHROOM = 'BATHROOM', 'Bathroom'
        TOILET = 'TOILET', 'Toilet'
        LAUNDRY = 'LAUNDRY', 'Laundry'
        GARDEN = 'GARDEN', 'Garden'
        GARAGE = 'GARAGE', 'Garage'

    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.KITCHEN,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.room_type}"


class Property(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    type = models.ForeignKey(PropertyTypes,
                             on_delete=models.CASCADE)

    room_types = models.ManyToManyField(RoomTypes,
                                        blank=True,
                                        null=True)

    num_people = models.PositiveIntegerField(default=0)

    client_number = models.ForeignKey(ClientNumber,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return f"Property owned by {self.user} - {self.type}"


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
    VALUE_MAX_DIGITS = 10  # Total number of digits (including those after the decimal)
    VALUE_DECIMAL_PLACES = 3  # Number of digits after the decimal point

    water_meter = models.ForeignKey(WaterMeter,
                                    on_delete=models.CASCADE,
                                    related_name='water_meter_readings')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='water_meter_readings')

    value = models.DecimalField(
        max_digits=VALUE_MAX_DIGITS,
        decimal_places=VALUE_DECIMAL_PLACES,
        validators=[MinValueValidator(0)]
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reading {self.value} for {self.water_meter} by {self.user}"

    def save(self, *args, **kwargs):
        if self.pk:
            last_reading = WaterMeterReading.objects.filter(
                water_meter=self.water_meter,
                date__lt=self.date
            ).order_by('-date').first()

            if last_reading and (self.value < last_reading.value or self.value > last_reading.value + 1000):
                raise ValidationError(
                    "The value should not be less than the previous reading or greater "
                    "than 1000 to the last saved reading."
                )

        super().save(*args, **kwargs)
