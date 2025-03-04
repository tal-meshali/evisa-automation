import datetime

from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Batch
from rest_framework.decorators import action

from api.models.documents.document_validation import DocumentValidationSerializer
from api.serializers.batch_serializer import BatchSerializer
from api.views.batches.batch_form import batch_form
from api.views.forms.form_arguments_mixin import FormArgumentsMixin


class BatchViewSet(viewsets.ModelViewSet, FormArgumentsMixin):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    form = batch_form

    def _create(self, request):
        data = request.data
        data["arrival_date"] = datetime.datetime.strptime(
            data["arrival_date"], "%d/%m/%y"
        )
        data["departure_date"] = datetime.datetime.strptime(
            data["departure_date"], "%d/%m/%y"
        )
        return Response(BatchSerializer(Batch.objects.create(**data)).data)

    @action(methods=["PUT"], detail="Parse all documents attached to the batch")
    def parse(self, request, pk):
        beneficiaries = self.get_object().beneficiary_set.all()
        result = {}
        for beneficiary in beneficiaries:
            result[beneficiary.id] = {
                "passport": DocumentValidationSerializer(
                    beneficiary.passport.parse()
                ).data,
                "portrait": DocumentValidationSerializer(
                    beneficiary.portrait.parse()
                ).data,
            }
        return Response(result)
