from dataclasses import dataclass

from rest_framework import serializers

from api.models.documents.upload_status import UploadStatus


@dataclass
class DocumentValidation:
    status: UploadStatus
    message: str
    image: str = None


class DocumentValidationSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.CharField()
    image = serializers.CharField()

    def get_status(self, obj: DocumentValidation):
        return obj.status.name
