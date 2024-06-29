from rest_framework import permissions
from .beneficiary_related_view_set import BeneficiaryRelatedViewSet
from ..models import PassportDetails
from ..serializers import PassportSerializer


class PassportViewSet(BeneficiaryRelatedViewSet):
    queryset = PassportDetails.objects.all()
    serializer_class = PassportSerializer
    # permission_classes = [permissions.IsAuthenticated]
