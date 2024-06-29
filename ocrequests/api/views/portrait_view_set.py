from rest_framework import permissions
from .beneficiary_related_view_set import BeneficiaryRelatedViewSet
from ..models import PortraitDetails
from ..serializers import PortraitSerializer


class PortraitViewSet(BeneficiaryRelatedViewSet):
    queryset = PortraitDetails.objects.all()
    serializer_class = PortraitSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "portrait_id"
