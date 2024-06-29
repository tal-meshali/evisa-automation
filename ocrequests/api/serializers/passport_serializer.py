from rest_framework import serializers
from ..models import PassportDetails, Beneficiary
from ..visa_requests.pipelines.general import PassportDetailsPipeline
from google.cloud.vision import ImageAnnotatorClient


class PassportSerializer(serializers.Serializer):
    passport_image = serializers.ImageField()
    created = serializers.DateTimeField(required=False)
    client = ImageAnnotatorClient()
    pipeline = PassportDetailsPipeline(client)

    def create(self, validated_data):
        passport = PassportDetails.objects.create(
            passport_image=validated_data["passport_image"],
            **self.pipeline.activate(validated_data["passport_image"])
        )
        passport.save()
        Beneficiary.objects.get(pk=validated_data["beneficiary"]).save_item(passport)
        return passport

    def update(self, instance, validated_data):
        instance.portrait_image = self.pipeline.activate(
            validated_data.get("passport_image", instance.passport_image)
        )
        instance.created = validated_data.get("created", instance.created)
        return instance
