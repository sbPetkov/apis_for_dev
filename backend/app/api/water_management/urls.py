from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterCompanyViewSet, ClientNumberViewSet, UserWaterMetersAPIView, PropertyCreateView, \
    PropertyDetailView, PropertyRoomsView, PropertyRoomDetailView, WaterMeterReadingView, PropertyTypeListView, \
    ClientNumberAverageConsumptionView, WaterMeterReadingDetailView

# Create a router for WaterCompanyViewSet
water_company_router = DefaultRouter()
water_company_router.register(r'water-companies', WaterCompanyViewSet)

# Create a router for ClientNumberViewSet
client_number_router = DefaultRouter()
client_number_router.register(r'client-numbers', ClientNumberViewSet)

urlpatterns = [
    path('', include(water_company_router.urls)),
    path('', include(client_number_router.urls)),
    path('user-water-meters/', UserWaterMetersAPIView.as_view(), name='user-water-meters'),
    path('properties/', PropertyCreateView.as_view(), name='create_property'),
    path('properties/<int:id>/', PropertyDetailView.as_view(), name='property-get-put-delete'),
    path('properties/<int:property_id>/rooms/', PropertyRoomsView.as_view(), name='property-rooms-view'),
    path('properties/<int:property_id>/rooms/<int:room_id>/', PropertyRoomDetailView.as_view(),
         name='property-room-detail'),
    path('properties/<int:property_id>/water-meter-readings/', WaterMeterReadingView.as_view(),
         name='water-meter-readings'),
    path('water-meter-readings/<int:pk>/', WaterMeterReadingDetailView.as_view(), name='water_meter_reading_detail'),
    path('property-types/', PropertyTypeListView.as_view(), name='property-type-list'),
    path('client-numbers/<int:client_number_id>/average-consumption/', ClientNumberAverageConsumptionView.as_view(),
         name='client-number-average-consumption'),
]
