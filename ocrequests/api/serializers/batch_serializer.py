from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .beneficiary_serializer import BeneficiarySerializer
from ..models import Batch


class BatchSerializer(ModelSerializer):
    created = serializers.DateTimeField(required=False)
    beneficiary_set = BeneficiarySerializer(read_only=True, allow_null=True)

    class Meta:
        model = Batch
        fields = ["id", "beneficiary_set", "created"]
        depth = 1
