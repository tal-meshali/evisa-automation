import base64
from abc import abstractmethod, ABC

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Beneficiary
from api.models.documents.document import Document
from api.models.documents.document_validation import (
    DocumentValidation,
    DocumentValidationSerializer,
)
from api.models.documents.passport import Passport
from api.models.documents.portrait import Portrait
from api.models.documents.upload_status import UploadStatus


class BeneficiaryDocumentViewSet(viewsets.ViewSet, ABC):
    lookup_url_kwarg = "document_key"
    class_name: str

    def get_beneficiary(self) -> Beneficiary:
        return Beneficiary.objects.get(
            pk=self.kwargs["_beneficiary_id"], batch__id=self.kwargs["batch_pk"]
        )

    @property
    def upload_message(self):
        return f"Uploaded {self.class_name[0].upper() + self.class_name[1:]}"

    @abstractmethod
    def nullify_document(self) -> None:
        pass

    @abstractmethod
    def add_document(self, beneficiary: Beneficiary, document) -> Document:
        pass

    @abstractmethod
    def get_document(self) -> Document:
        pass

    @action(methods=["POST"], detail=False)
    def parse_document(self, request, *args, **kwargs):
        return self.get_document().parse()

    @action(methods=["DELETE"], detail=False)
    def delete_document(self, request, *args, **kwargs):
        self.nullify_document()
        beneficiary = self.get_beneficiary()
        beneficiary.save()
        return Response()

    @action(methods=["PUT"], detail=False)
    def upload_document(self, request, *args, **kwargs):
        beneficiary = self.get_beneficiary()
        batch = beneficiary.batch
        document = self.add_document(beneficiary, list(request.data.values())[0])
        beneficiary.save()
        if batch.ready_to_parse:
            return DocumentValidationSerializer(document.parse()).data
        image = document.image
        image.seek(0)
        return Response(
            DocumentValidationSerializer(
                DocumentValidation(
                    image=f"data:image/jpeg;base64,{base64.b64encode(image.read()).decode()}",
                    message=self.upload_message,
                    status=UploadStatus.Uploaded,
                )
            ).data
        )


class BeneficiaryPortraitViewSet(BeneficiaryDocumentViewSet):
    class_name = "portrait"

    def get_document(self) -> Document:
        return self.get_beneficiary().portrait

    def nullify_document(self) -> None:
        self.get_beneficiary().portrait = None

    def add_document(self, beneficiary, document) -> Document:
        beneficiary.portrait = Portrait.objects.create(image=document)
        return beneficiary.portrait


class BeneficiaryPassportViewSet(BeneficiaryDocumentViewSet):
    class_name = "passport"

    def get_document(self) -> Document:
        return self.get_beneficiary().passport

    def nullify_document(self) -> None:
        self.get_beneficiary().passport = None

    def add_document(self, beneficiary, document) -> Document:
        beneficiary.passport = Passport.objects.create(image=document)
        return beneficiary.passport
