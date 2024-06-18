import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests
from PIL import Image
from io import BytesIO

from api.profiles_api.models import Profile


def get_facebook_user_data(access_token):
    url = 'https://graph.facebook.com/me'
    params = {
        'fields': 'id,first_name,last_name,email,picture',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    user_data = response.json()

    if 'error' in user_data:
        raise ValueError('Error fetching data from Facebook: {}'.format(user_data['error']))

    return user_data


def create_or_get_user(user_data):
    email = user_data.get('email')

    if not email:
        raise ValueError("Email is required")

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        user = User(username=email)
        user.set_unusable_password()
        user.save()

    profile = Profile(user=user)

    profile_pic = requests.get(user_data['picture']['data']['url'])

    if profile_pic.status_code == 200:
        img = Image.open(BytesIO(profile_pic.content))
        img = img.convert("RGBA")

        avatar_name = f"{user.pk}.png"
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        in_memory_uploaded_file = InMemoryUploadedFile(
            img_io, None, avatar_name, 'image/png', sys.getsizeof(img_io), None
        )

        profile.first_name = user_data.get('first_name', '')
        profile.last_name = user_data.get('last_name', '')
        profile.email = user_data.get('email', '')
        profile.date_joined = timezone.now()
        profile.profile_picture = in_memory_uploaded_file

    profile.save()

    return user


@api_view(['POST'])
@permission_classes([AllowAny])
def facebook_login(request):
    if request.method == 'POST':
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = get_facebook_user_data(access_token)

        if not user_data:
            return Response({'error': 'Invalid Facebook access token'}, status=status.HTTP_400_BAD_REQUEST)

        user = create_or_get_user(user_data)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)