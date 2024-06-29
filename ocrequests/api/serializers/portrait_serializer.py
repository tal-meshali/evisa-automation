from rest_framework import serializers
from ..models import PortraitDetails
from ..utility.serializer_helpers import add_beneficiary
from ..visa_requests.pipelines.image import PortraitImagePipeline
from google.cloud.vision import ImageAnnotatorClient


class PortraitSerializer(serializers.Serializer):
    portrait_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PortraitImagePipeline(client)

    @add_beneficiary
    def create(self, validated_data):
        return PortraitDetails.objects.create(
            portrait_image=self.pipeline.activate(validated_data["portrait_image"]),
        )

    def update(self, instance, validated_data):
        instance.portrait_image = self.pipeline.activate(
            validated_data.get("portrait_image", instance.portrait_image)
        )
        return instance
