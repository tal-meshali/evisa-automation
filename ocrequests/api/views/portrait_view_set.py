from rest_framework import permissions, viewsets
from ..models import PortraitDetails
from ..serializers import PortraitSerializer


class PortraitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PortraitDetails.objects.all()
    serializer_class = PortraitSerializer
    # permission_classes = [permissions.IsAuthenticated]
