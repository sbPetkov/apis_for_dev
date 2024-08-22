from django.contrib.auth.models import User
from rest_framework import serializers

from api.profiles_api.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'email',
            'city',
            'phone_number',
            'date_joined',
            'profile_picture',
            'language'
        )


class DeactivateAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.is_active = False
        user.save()
        return user
