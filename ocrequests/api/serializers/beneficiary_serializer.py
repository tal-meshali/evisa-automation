from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Beneficiary
from ..serializers import PassportSerializer, PortraitSerializer


class BeneficiarySerializer(ModelSerializer):
    portrait = PortraitSerializer(allow_null=True)
    passport = PassportSerializer(allow_null=True)
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Beneficiary
        fields = ["id", "portrait", "passport", "created"]
