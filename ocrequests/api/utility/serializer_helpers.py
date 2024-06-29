from rest_framework.exceptions import APIException
from ..visa_requests.pipelines.pipeline import ParsingException
from ..models import Beneficiary


def vision_model_validator(method):
    def wrapper(self, serializer):
        try:
            return method(self, serializer)
        except ParsingException as e:
            raise APIException(detail=e.args[0])

    return wrapper


def add_beneficiary(method):
    def wrapper(self, validated_data):
        model = method(self, validated_data)
        model.save()
        Beneficiary.objects.get(pk=validated_data["beneficiary"]).save_item(model)
        return model

    return wrapper
