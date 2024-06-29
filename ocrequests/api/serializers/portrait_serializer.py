from rest_framework import serializers
from ..models import PortraitDetails, Beneficiary
from ..visa_requests.pipelines.image import PortraitImagePipeline
from google.cloud.vision import ImageAnnotatorClient


class PortraitSerializer(serializers.Serializer):
    portrait_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PortraitImagePipeline(client)

    def create(self, validated_data):
        portrait = PortraitDetails.objects.create(
            portrait_image=self.pipeline.activate(validated_data["portrait_image"]),
        )
        portrait.save()
        Beneficiary.objects.get(pk=validated_data["beneficiary"]).save_item(portrait)
        return portrait

    def update(self, instance, validated_data):
        instance.portrait_image = self.pipeline.activate(
            validated_data.get("portrait_image", instance.portrait_image)
        )
        return instance
