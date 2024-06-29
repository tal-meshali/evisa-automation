from rest_framework import viewsets
from ..models import Beneficiary
from ..serializers.beneficiary_serializer import BeneficiarySerializer


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    lookup_url_kwarg = "beneficiary_id"
