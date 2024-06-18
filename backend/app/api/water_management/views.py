from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WaterCompany, ClientNumber, WaterMeter
from .serializers import WaterCompanySerializer, ClientNumberSerializer, WaterMeterSerializer


class WaterCompanyViewSet(viewsets.ModelViewSet):
    queryset = WaterCompany.objects.all()
    serializer_class = WaterCompanySerializer


class ClientNumberViewSet(viewsets.ModelViewSet):
    queryset = ClientNumber.objects.all()
    serializer_class = ClientNumberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ClientNumber.objects.filter(users=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(users=[user])


class UserWaterMetersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        client_numbers = ClientNumber.objects.filter(users=user)
        water_meters = WaterMeter.objects.filter(client_number__in=client_numbers)
        serializer = WaterMeterSerializer(water_meters, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        client_number_value = request.data.get('client_number')
        meter_number = request.data.get('meter_number')

        if not client_number_value or not meter_number:
            return Response(
                {"detail": "Client number and meter number are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        client_number = get_object_or_404(ClientNumber, client_number=client_number_value, users=user)
        water_meter = WaterMeter(client_number=client_number, meter_number=meter_number)
        water_meter.save()

        return Response(
            {"detail": "Water meter created successfully."},
            status=status.HTTP_201_CREATED
        )