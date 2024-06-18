from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterCompanyViewSet, ClientNumberViewSet, UserWaterMetersAPIView

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

]
