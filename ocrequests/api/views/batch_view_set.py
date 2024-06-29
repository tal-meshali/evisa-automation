from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Batch, Beneficiary
from rest_framework.decorators import action

from ..serializers.batch_serializer import BatchSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    @action(methods=["POST"], detail="Append a beneficiary to the batch's list")
    def create_beneficiary(self, request, pk):
        beneficiary = Beneficiary.objects.create()
        beneficiary.related_batch = self.get_object()
        beneficiary.save()
        return Response({"created": model_to_dict(beneficiary)})

    @action(
        methods=["GET"], detail="Get all of the beneficiaries attached to the batch"
    )
    def get_beneficiaries(self, request, pk):
        beneficiaries = self.get_object().beneficiary_set.all()
        return Response(
            {"received": [model_to_dict(beneficiary) for beneficiary in beneficiaries]}
        )
