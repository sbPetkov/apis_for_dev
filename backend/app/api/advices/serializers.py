from rest_framework import serializers
from .models import Advice


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ['id', 'title', 'background_image', 'content', 'position', 'created_at', 'updated_at']
