from abc import ABC

from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet

from ..utility.serializer_helpers import vision_model_validator


class BeneficiaryRelatedViewSet(ModelViewSet, ABC):
    def get_queryset(self):
        return self.queryset.filter(beneficiary=self.kwargs["beneficiary_id"])

    @vision_model_validator
    def perform_create(self, serializer):
        serializer.save(beneficiary=self.kwargs["beneficiary_id"])
