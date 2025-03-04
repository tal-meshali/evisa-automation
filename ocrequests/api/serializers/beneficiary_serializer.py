from rest_framework.serializers import ModelSerializer

from .document_serializer import DocumentSerializer
from ..models import Beneficiary


class BeneficiarySerializer(ModelSerializer):
    portrait = DocumentSerializer()
    passport = DocumentSerializer()

    class Meta:
        model = Beneficiary
        fields = ["id", "portrait", "passport"]
