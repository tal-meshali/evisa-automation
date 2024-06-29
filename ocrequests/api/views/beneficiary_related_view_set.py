from abc import ABC
from rest_framework.viewsets import ModelViewSet


class BeneficiaryRelatedViewSet(ModelViewSet, ABC):
    def get_queryset(self):
        return self.queryset.filter(beneficiary=self.kwargs["beneficiary_id"])

    def perform_create(self, serializer):
        serializer.save(beneficiary=self.kwargs["beneficiary_id"])
