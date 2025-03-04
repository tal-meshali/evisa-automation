from dataclasses import dataclass
from rest_framework import serializers


@dataclass
class ValidationResult:
    valid: bool
    validation_output: str = None


class ValidationResultSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    validation_output = serializers.CharField()
