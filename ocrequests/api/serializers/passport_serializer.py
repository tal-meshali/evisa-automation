from rest_framework import serializers
from ..models import PassportDetails
from ..visa_requests.pipelines.general import PassportDetailsPipeline
from google.cloud.vision import ImageAnnotatorClient

class PassportSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    passport_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PassportDetailsPipeline(client)

    def create(self, validated_data):
        return PassportDetails.objects.create(email_address=validated_data["email_address"],
                                              passport_image=validated_data["passport_image"],
                                              **self.pipeline.activate(validated_data["passport_image"]))

    def update(self, instance, validated_data):
        instance.email_address = validated_data.get('email_address', instance.email_address)
        instance.portrait_image = validated_data.get('portrait_image', instance.portrait_image)
        instance.created = validated_data.get('created', instance.created)
        return instance
