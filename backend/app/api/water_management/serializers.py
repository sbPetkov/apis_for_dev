from rest_framework import serializers
from .models import WaterCompany, ClientNumber, WaterMeter


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
        fields = ['client_number', 'meter_number']
