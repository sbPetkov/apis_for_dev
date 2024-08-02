from rest_framework import serializers
from .models import WaterCompany, ClientNumber, WaterMeter, Property, PropertyTypes, RoomTypes, WaterMeterReading


class WaterCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterCompany
        fields = ['id', 'name', 'phone_number', 'email']


class ClientNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientNumber
        fields = '__all__'


class WaterMeterSerializer(serializers.ModelSerializer):
    client_number = serializers.CharField(source='client_number.client_number')

    class Meta:
        model = WaterMeter
        fields = ['id', 'client_number', 'meter_number']


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ['id', 'type', 'image']


class PropertySerializer(serializers.ModelSerializer):
    type = PropertyTypeSerializer()
    client_number = ClientNumberSerializer()
    water_meters = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ('id', 'type', 'num_people', 'client_number', 'water_meters')

    def get_water_meters(self, obj):
        water_meters_qs = WaterMeter.objects.filter(client_number=obj.client_number)
        return WaterMeterSerializer(water_meters_qs, many=True).data


class RoomTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypes
        fields = '__all__'


class WaterMeterReadingSerializer(serializers.ModelSerializer):
    water_meter_id = serializers.IntegerField(source='water_meter.id', read_only=True)

    class Meta:
        model = WaterMeterReading
        fields = ['id', 'water_meter_id', 'user', 'value', 'date']
        read_only_fields = ['user']


class WaterMeterAverageConsumptionSerializer(serializers.Serializer):
    approximate = serializers.BooleanField()
    average_monthly_consumption = serializers.FloatField()
    num_people = serializers.IntegerField()
    average_usage_per_person_per_week = serializers.FloatField()
    average_usage_per_room = serializers.DictField(child=serializers.FloatField())


