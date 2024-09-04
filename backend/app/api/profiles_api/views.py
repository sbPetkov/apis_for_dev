from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.profiles_api.tasks import update_rankings

from api.profiles_api.models import Profile, UserRank
from api.profiles_api.serializers import UserSerializer, ProfileSerializer, DeactivateAccountSerializer, ChangePasswordSerializer, UserRankSerializer
from rest_framework.views import APIView


@permission_classes([AllowAny])
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        headers = self.get_success_headers(user_serializer.data)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProfileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found")


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_200_OK)


class DeactivateAccountView(generics.GenericAPIView):
    serializer_class = DeactivateAccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Account has been deactivated."}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Set the new password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRankingView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the authenticated user from the request

        try:
            user_rank = user.user_rank  # Assuming a OneToOne relationship with the UserRank model

            if user_rank.town_rank == 0 or user_rank.company_rank == 0:
                return Response({'error': 'Insufficient data to calculate rank.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserRankSerializer(user_rank)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserRank.DoesNotExist:
            return Response({'error': 'Rank data not found for user.'}, status=status.HTTP_404_NOT_FOUND)


class TriggerUpdateRankingsView(View):
    def get(self, request, *args, **kwargs):
        update_rankings()
        return JsonResponse({'status': 'Rankings update triggered'}, status=200)