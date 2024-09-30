from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from api.profiles_api.models import Profile, UserRank


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def create(self, validated_data):
        email = validated_data.get('username')

        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

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
            'language',
            'push',
            'email_notification',
            'daily',
            'weekly',
            'monthly',
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value


class UserRankSerializer(serializers.ModelSerializer):
    water_company_name = serializers.SerializerMethodField()

    class Meta:
        model = UserRank
        fields = ['town_rank', 'company_rank', 'last_updated', 'water_company_name']

    def get_water_company_name(self, obj):
        # Access the user from the UserRank model (assuming OneToOneField relation)
        user = obj.user

        # Fetch the related water company through the client numbers
        client_numbers = user.client_numbers.all()
        if not client_numbers:
            return None

        # Return the first related water company name (or adjust logic as needed)
        return client_numbers.first().water_company.name