from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, generics
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WaterCompany, ClientNumber, WaterMeter, PropertyTypes, Property, RoomTypes, WaterMeterReading
from .serializers import WaterCompanySerializer, ClientNumberSerializer, WaterMeterSerializer, PropertySerializer, \
    RoomTypesSerializer, WaterMeterReadingSerializer, PropertyTypeSerializer, WaterMeterAverageConsumptionSerializer


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


class PropertyTypeListView(APIView):
    def get(self, request):
        property_types = PropertyTypes.objects.all()
        serializer = PropertyTypeSerializer(property_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PropertyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(user=request.user)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        try:
            property_type = PropertyTypes.objects.get(id=data['property_type']['id'])
        except PropertyTypes.DoesNotExist:
            return Response({'error': 'Property type not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            water_company = WaterCompany.objects.get(id=data['water_company']['id'])
        except WaterCompany.DoesNotExist:
            return Response({'error': 'Water company not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        client_number_data = data['client_number']
        client_number = ClientNumber.objects.create(water_company=water_company,
                                                    client_number=client_number_data['client_number'])
        client_number.users.set(client_number_data['users'])

        property_data = data['property']
        property = Property.objects.create(user=request.user,
                                           type=property_type,
                                           num_people=property_data['num_people'],
                                           client_number=client_number)

        # Create Water Meters
        water_meters_data = data.get('water_meters', [])
        water_meters = []
        for meter_number in water_meters_data:
            water_meter = WaterMeter.objects.create(
                client_number=client_number,
                meter_number=meter_number
            )
            water_meters.append(water_meter)

        # Serialize Property and Water Meters
        property_serializer = PropertySerializer(property)
        water_meter_serializers = [WaterMeterSerializer(water_meter).data for water_meter in water_meters]

        return Response({
            "property": property_serializer.data,
            "water_meters": water_meter_serializers
        }, status=status.HTTP_201_CREATED)


class PropertyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(Property.objects.select_related('type', 'client_number'), id=id)

    def get(self, request, id):
        property_instance = self.get_object(id)
        serializer = PropertySerializer(property_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        property_instance = self.get_object(id)
        serializer = PropertySerializer(property_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        property_instance = self.get_object(id)
        property_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PropertyRoomsView(APIView):
    def get_property(self, property_id):
        try:
            return Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise serializers.ValidationError({'error': 'Property not found'})

    def get(self, request, property_id):
        property_instance = self.get_property(property_id)
        room_types = property_instance.room_types.all()
        serializer = RoomTypesSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, property_id):
        property_instance = self.get_property(property_id)
        data = request.data

        # Validate incoming data
        serializer = RoomTypesSerializer(data=data)
        if serializer.is_valid():
            room_type = serializer.save()
            property_instance.room_types.add(room_type)
            property_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyRoomDetailView(APIView):
    def get_property(self, property_id):
        try:
            return Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise serializers.ValidationError({'error': 'Property not found'})

    def get_room(self, property_instance, room_id):
        try:
            return property_instance.room_types.get(id=room_id)
        except RoomTypes.DoesNotExist:
            raise serializers.ValidationError({'error': 'Room not found'})

    def get(self, request, property_id, room_id):
        property_instance = self.get_property(property_id)
        room_instance = self.get_room(property_instance, room_id)
        serializer = RoomTypesSerializer(room_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, property_id, room_id):
        property_instance = self.get_property(property_id)
        room_instance = self.get_room(property_instance, room_id)

        # Update the room instance with new data
        serializer = RoomTypesSerializer(room_instance, data=request.data, partial=True)
        if serializer.is_valid():
            # Remove the old room instance
            property_instance.room_types.remove(room_instance)

            # Save the new room instance
            updated_room = serializer.save()

            # Add the new room instance to the property
            property_instance.room_types.add(updated_room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, property_id, room_id):
        property_instance = self.get_property(property_id)
        room_instance = self.get_room(property_instance, room_id)
        property_instance.room_types.remove(room_instance)
        room_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WaterMeterReadingView(APIView):
    def post(self, request, property_id):
        property_instance = get_object_or_404(Property, id=property_id)
        client_number = property_instance.client_number
        water_meters = client_number.water_meters.all()

        readings_data = request.data.get('readings', [])
        readings = []

        for reading_data in readings_data:
            water_meter_id = reading_data.get('water_meter_id')
            value = reading_data.get('value')

            water_meter = water_meters.filter(id=water_meter_id).first()
            if not water_meter:
                return Response({'error': f'Water meter with id {water_meter_id} not found'},
                                status=status.HTTP_404_NOT_FOUND)

            reading = WaterMeterReading(
                water_meter=water_meter,
                user=request.user,
                value=value
            )
            reading.save()
            readings.append(reading)

        serializer = WaterMeterReadingSerializer(readings, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, property_id):
        property_instance = get_object_or_404(Property, id=property_id)
        client_number = property_instance.client_number
        water_meters = client_number.water_meters.all()

        readings = WaterMeterReading.objects.filter(water_meter__in=water_meters)
        serializer = WaterMeterReadingSerializer(readings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WaterMeterReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterMeterReading.objects.all()
    serializer_class = WaterMeterReadingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientNumberAverageConsumptionView(APIView):
    def get(self, request, client_number_id):
        client_number = get_object_or_404(ClientNumber, id=client_number_id)
        property_instance = client_number.property_set.first()  # Assuming a one-to-one relationship
        water_meters = client_number.water_meters.all()

        total_value_diff = 0
        total_days_diff = 0
        insufficient_data = False

        for water_meter in water_meters:
            average_consumption = water_meter.calculate_average_monthly_consumption()
            if isinstance(average_consumption, str):
                insufficient_data = True
                continue

            value_diff = average_consumption['average_monthly_consumption'] / 30 * (average_consumption['approximate'] * 30 + (not average_consumption['approximate'] * 1))
            days_diff = 30 if average_consumption['approximate'] else 1

            total_value_diff += value_diff
            total_days_diff += days_diff

        if insufficient_data and total_days_diff == 0:
            return Response({'error': 'Not enough data to calculate average monthly consumption for some or all meters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        average_daily_consumption = total_value_diff / total_days_diff
        combined_average_monthly_consumption = average_daily_consumption * 30
        combined_average_monthly_consumption = round(combined_average_monthly_consumption, 3)

        num_people = property_instance.num_people if property_instance else 0
        average_usage_per_person_per_week = round(combined_average_monthly_consumption / num_people / 4, 3) if num_people else 0

        rooms = property_instance.room_types.all() if property_instance else []
        num_rooms = rooms.count()
        average_usage_per_room = round(combined_average_monthly_consumption / num_rooms, 3) if num_rooms else 0

        room_usage = {room.name: average_usage_per_room for room in rooms}

        result = {
            "approximate": total_days_diff < 30,
            "average_monthly_consumption": combined_average_monthly_consumption,
            "num_people": num_people,
            "average_usage_per_person_per_week": average_usage_per_person_per_week,
            "average_usage_per_room": room_usage
        }

        serializer = WaterMeterAverageConsumptionSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
