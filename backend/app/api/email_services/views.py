from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from .serializers import EmailRequestSerializer
from ..water_management.models import WaterCompany


class SendEmailAPIView(generics.GenericAPIView):
    serializer_class = EmailRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from the validated request
        issue = serializer.validated_data['issue']
        address = serializer.validated_data['address']
        water_company_id = serializer.validated_data['water_company_id']
        content = serializer.validated_data['content']

        # Get the authenticated user
        user = request.user
        user_phone_number = user.profile.phone_number

        try:
            # Get the WaterCompany instance
            water_company = WaterCompany.objects.get(id=water_company_id)
        except WaterCompany.DoesNotExist:
            return Response({"error": "WaterCompany not found"}, status=status.HTTP_404_NOT_FOUND)

        # Construct the email content
        email_subject = f"Докладване на проблем: {issue}"
        email_message = (
            f"Вид: {issue}\n"
            f"Адрес: {address}\n"
            f"E-mail: {user.username}\n"
            f"Телефон: {user_phone_number}\n\n"
            f"Детайли:\n{content}"
        )
        recipient_email = water_company.email

        # Send the email
        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
        )

        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
