from rest_framework import permissions, viewsets
from ..models import PassportDetails
from ..serializers import PassportSerializer


class PassportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PassportDetails.objects.all()
    serializer_class = PassportSerializer
    # permission_classes = [permissions.IsAuthenticated]
