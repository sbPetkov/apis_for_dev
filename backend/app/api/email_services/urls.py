from django.urls import path
from .views import SendEmailAPIView

urlpatterns = [
    path('report/', SendEmailAPIView.as_view(), name='send-email'),
]
