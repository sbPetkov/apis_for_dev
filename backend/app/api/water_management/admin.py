from django.contrib import admin
from .models import ClientNumber, WaterMeter, WaterMeterReading, WaterCompany


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


@admin.register(WaterCompany)
class WaterCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
