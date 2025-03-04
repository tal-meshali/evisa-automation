from abc import abstractmethod
from typing import List

from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.forms.arguments.argument import Arg
from api.forms.validation.validation_result import ValidationResultSerializer


class FormArgumentsMixin(ViewSet):
    form: List[Arg]

    @action(methods=["GET"], detail=False)
    def arguments(self, request):
        return Response([arg.structure() for arg in self.form])

    @action(methods=["POST"], detail=False)
    def validate(self, request, raise_exception=False):
        arg_name_to_value = request.data
        results = {}
        for arg in self.form:
            arg.value = arg_name_to_value[arg.name]
            results[arg.name] = arg.validate(arg.value)
            if raise_exception and not results[arg.name].valid:
                raise APIException()
        return Response(
            {
                "validation": {
                    name: ValidationResultSerializer(item).data
                    for name, item in results.items()
                },
                "valid": all([validation.valid for validation in results.values()]),
            }
        )

    @action(methods=["POST"], detail=False)
    def send(self, request):
        self.validate(request, True)
        return self._create(request)

    @abstractmethod
    def _create(self, request):
        pass
