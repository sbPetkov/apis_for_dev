from rest_framework import serializers
from .models import WaterCompany, ClientNumber


class WaterCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterCompany
        fields = ['id', 'name', 'phone_number', 'email']


class ClientNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientNumber
        fields = '__all__'

