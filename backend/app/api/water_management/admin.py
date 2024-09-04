from django.contrib import admin
from .models import ClientNumber, WaterMeter, WaterMeterReading, WaterCompany, Property, RoomTypes, PropertyTypes, \
    ConsumptionAdvice


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


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'num_people', 'client_number')


@admin.register(RoomTypes)
class RoomTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type')


@admin.register(PropertyTypes)
class PropertyTypesAdmin(admin.ModelAdmin):
    list_display = ('type', 'image')


@admin.register(ConsumptionAdvice)
class ConsumptionAdviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_value', 'max_value', 'image_preview')
    search_fields = ('title',)
    list_filter = ('min_value', 'max_value')

    def image_preview(self, obj):
        return obj.image.url if obj.image else 'No Image'
    image_preview.short_description = 'Image Preview'
