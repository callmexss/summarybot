from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Document, DocumentChunk, DocumentReview
from .serializers import (
    DocumentChunkSerializer,
    DocumentSerializer,
    DocumentReviewSerializer,
)
from .tasks import (
    handle_uploaded_file,
    handle_uploaded_url,
    process_document_chunks,
    review_document_chunks,
)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request):
        source = request.data.get("source", None)
        uploaded_file = request.data.get("file_path", None)

        if source:
            task = handle_uploaded_url.apply_async((source,), countdown=1)
            return Response({"task_id": str(task.id)}, status=status.HTTP_202_ACCEPTED)

        elif uploaded_file:
            task = handle_uploaded_file.apply_async((uploaded_file,), countdown=1)
            return Response({"task_id": str(task.id)}, status=status.HTTP_202_ACCEPTED)

        else:
            return Response(
                {"error": "Either 'source' or 'file' is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DocumentChunkViewSet(viewsets.ModelViewSet):
    queryset = DocumentChunk.objects.all()
    serializer_class = DocumentChunkSerializer

    def get_queryset(self):
        document_id = self.kwargs["document_pk"]
        return DocumentChunk.objects.filter(document_id=document_id)

    def create(self, request, *args, **kwargs):
        document_id = self.kwargs.get("document_pk")
        if document_id:
            task = process_document_chunks.apply_async((document_id,), countdown=1)
            return Response({"task_id": str(task.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Document ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )


class DocumentReviewViewSet(viewsets.ModelViewSet):
    queryset = DocumentReview.objects.all()
    serializer_class = DocumentReviewSerializer

    def create(self, request, *args, **kwargs):
        document_id = self.kwargs.get("document_pk")
        if document_id:
            task = review_document_chunks.apply_async((document_id,), countdown=1)
            return Response({"task_id": str(task.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Document ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
