from rest_framework import serializers
from .models import Document, DocumentChunk, DocumentReview


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = "__all__"


class DocumentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentReview
        fields = "__all__"
