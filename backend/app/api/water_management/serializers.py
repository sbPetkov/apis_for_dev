from rest_framework import serializers
from .models import WaterCompany, ClientNumber, WaterMeter, Property, PropertyTypes, RoomTypes, WaterMeterReading, \
    ConsumptionAdvice


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


class PropertyUpdateSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=PropertyTypes.objects.all(), required=False)
    client_number = serializers.PrimaryKeyRelatedField(queryset=ClientNumber.objects.all(), required=False)
    water_meters = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Property
        fields = ('type', 'num_people', 'client_number', 'water_meters')

    def update(self, instance, validated_data):
        # Update type
        type_instance = validated_data.pop('type', None)
        if type_instance:
            instance.type = type_instance

        # Update client_number
        client_number_instance = validated_data.pop('client_number', None)
        if client_number_instance:
            instance.client_number = client_number_instance

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle water meters
        water_meters_data = validated_data.get('water_meters', None)
        if water_meters_data is not None:
            instance.water_meters.clear()  # Clear existing water meters
            for meter_number in water_meters_data:
                water_meter = WaterMeter.objects.get(meter_number=meter_number)
                instance.water_meters.add(water_meter)

        instance.save()
        return instance


class ConsumptionAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionAdvice
        fields = ['id', 'title', 'image', 'min_value', 'max_value']


class RoomTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypes
        fields = '__all__'


class WaterMeterReadingSerializer(serializers.ModelSerializer):
    water_meter_id = serializers.IntegerField(source='water_meter.id', read_only=True)
    water_meter_number = serializers.CharField(source='water_meter.meter_number', read_only=True)

    class Meta:
        model = WaterMeterReading
        fields = ['id', 'water_meter_id', 'water_meter_number', 'user', 'value', 'date']
        read_only_fields = ['user']


class WaterMeterReadingWithPropertySerializer(serializers.ModelSerializer):
    water_meter_id = serializers.IntegerField(source='water_meter.id', read_only=True)
    water_meter_number = serializers.CharField(source='water_meter.meter_number', read_only=True)
    property_type = serializers.SerializerMethodField()

    class Meta:
        model = WaterMeterReading
        fields = ['id', 'water_meter_id', 'water_meter_number', 'property_type', 'user', 'value', 'date']
        read_only_fields = ['user']

    def get_property_type(self, obj):
        # Get the Property object using the ClientNumber from the WaterMeter
        property_obj = Property.objects.filter(client_number=obj.water_meter.client_number).first()
        return property_obj.type.type if property_obj and property_obj.type else None


class WaterMeterAverageConsumptionSerializer(serializers.Serializer):
    approximate = serializers.BooleanField()
    average_monthly_consumption = serializers.FloatField()
    num_people = serializers.IntegerField()
    average_usage_per_person_per_week = serializers.FloatField()
    average_usage_per_room = serializers.DictField(child=serializers.FloatField())
    max_water_usage_for_property_per_month = serializers.FloatField()
    current_water_usage_for_person_per_room = serializers.FloatField()




