from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WaterCompany, ClientNumber
from .serializers import WaterCompanySerializer, ClientNumberSerializer


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


class UserClientNumbersAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        client_numbers = ClientNumber.objects.filter(users=user)
        serializer = ClientNumberSerializer(client_numbers, many=True)
        return Response(serializer.data)
