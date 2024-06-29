from rest_framework import serializers
from ..models import PassportDetails
from ..utility.serializer_helpers import add_beneficiary
from ..visa_requests.pipelines.general import PassportDetailsPipeline
from google.cloud.vision import ImageAnnotatorClient


class PassportSerializer(serializers.Serializer):
    passport_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PassportDetailsPipeline(client)

    @add_beneficiary
    def create(self, validated_data):
        return PassportDetails.objects.create(
            passport_image=validated_data["passport_image"],
            **self.pipeline.activate(validated_data["passport_image"])
        )

    def update(self, instance, validated_data):
        instance.portrait_image = self.pipeline.activate(
            validated_data.get("passport_image", instance.passport_image)
        )
        instance.created = validated_data.get("created", instance.created)
        return instance
