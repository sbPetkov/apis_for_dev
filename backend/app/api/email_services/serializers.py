from rest_framework import serializers


class EmailRequestSerializer(serializers.Serializer):
    issue = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    water_company_id = serializers.IntegerField()
    content = serializers.CharField()
