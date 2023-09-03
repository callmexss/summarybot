from django.urls import path, include
from rest_framework_nested import routers

from .views import DocumentViewSet, DocumentChunkViewSet, DocumentReviewViewSet


router = routers.SimpleRouter()
router.register(r"documents", DocumentViewSet)

documents_router = routers.NestedSimpleRouter(router, r"documents", lookup="document")
documents_router.register(r"chunks", DocumentChunkViewSet, basename="document-chunks")
documents_router.register(
    r"reviews", DocumentReviewViewSet, basename="document-reviews"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(documents_router.urls)),
]
