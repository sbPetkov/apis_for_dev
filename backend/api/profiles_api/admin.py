from django.contrib import admin
from .models import Profile, ClientNumber, WaterMeter, WaterMeterReading


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'city', 'phone_number', 'date_joined')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'city', 'phone_number')
    readonly_fields = ('date_joined',)


@admin.register(ClientNumber)
class ClientNumberAdmin(admin.ModelAdmin):
    list_display = ('client_number',)
    search_fields = ('client_number',)


@admin.register(WaterMeter)
class WaterMeterAdmin(admin.ModelAdmin):
    list_display = ('meter_number', 'client_number')
    search_fields = ('meter_number', 'client_number__client_number')


@admin.register(WaterMeterReading)
class WaterMeterReadingAdmin(admin.ModelAdmin):
    list_display = ('value', 'water_meter', 'user', 'date')
    search_fields = ('water_meter__meter_number', 'user__username')