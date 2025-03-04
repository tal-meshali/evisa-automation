from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    image = serializers.ImageField()
