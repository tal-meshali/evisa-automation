from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .batch_view import BatchViewSet
from .beneficiary_view import BeneficiaryViewSet
from .document_view import BeneficiaryPortraitViewSet, BeneficiaryPassportViewSet

router = SimpleRouter()
router.register("batch", BatchViewSet, basename="batch")

beneficiary_router = NestedSimpleRouter(router, "batch", lookup="batch")
beneficiary_router.register(
    "beneficiaries", BeneficiaryViewSet, basename="beneficiaries"
)

document_router = NestedSimpleRouter(beneficiary_router, "beneficiaries", lookup="")
document_router.register("passport", BeneficiaryPassportViewSet, basename="passport")
document_router.register("portrait", BeneficiaryPortraitViewSet, basename="portrait")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(beneficiary_router.urls)),
    path("", include(document_router.urls)),
]
