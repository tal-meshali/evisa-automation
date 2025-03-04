from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Beneficiary, Batch
from api.models.documents.document import Document
from api.models.documents.passport import Passport
from api.models.documents.portrait import Portrait
from api.serializers.beneficiary_serializer import BeneficiarySerializer


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    lookup_url_kwarg = "beneficiary_id"

    def get_batch(self):
        return Batch.objects.get(pk=self.kwargs["batch_pk"])

    def get_queryset(self):
        return self.get_batch().beneficiaries

    def create(self, request, *args, **kwargs):
        beneficiary = Beneficiary.objects.create()
        ContentFile(request.data["passport"]["image"])
        beneficiary.passport = Passport.objects.create(
            image=ContentFile(
                request.data["passport"]["image"], name=f"passport_{beneficiary.id}"
            )
        )
        beneficiary.portrait = Portrait.objects.create(
            image=ContentFile(
                request.data["portrait"]["image"], name=f"portrait_{beneficiary.id}"
            )
        )
        batch = self.get_batch()
        beneficiary.batch = batch
        beneficiary.save()
        return Response(BeneficiarySerializer(beneficiary).data)
