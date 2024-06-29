from rest_framework import serializers
from ..models import PortraitDetails
from ..visa_requests.pipelines.image import PortraitImagePipeline
from google.cloud.vision import ImageAnnotatorClient


class PortraitSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    portrait_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PortraitImagePipeline(client)

    def create(self, validated_data):
        return PortraitDetails.objects.create(
            email_address=validated_data["email_address"],
            portrait_image=self.pipeline.activate(validated_data["portrait_image"]),
        )

    def update(self, instance, validated_data):
        instance.email_address = validated_data.get(
            "email_address", instance.email_address
        )
        instance.portrait_image = self.pipeline.activate(
            validated_data.get("portrait_image", instance.portrait_image)
        )
        return instance
