from django.contrib import admin
from .models import Document, DocumentChunk, DocumentReview


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "task", "file_path", "created_at", "updated_at")


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "chunk_content", "order")
    list_filter = ("document",)
    ordering = ("document", "order")


@admin.register(DocumentReview)
class DocumentReviewAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "task",
        "chunk_content_summary",
        "summary",
        "review",
        "order",
        "created_at",
        "updated_at",
    )
    list_filter = ("task",)
    ordering = (
        "task",
        "order",
    )
    search_fields = ("document__id",)
    readonly_fields = ("created_at", "updated_at")

    def chunk_content_summary(self, obj):
        return (
            obj.chunk_content[:200] + "..."
            if len(obj.chunk_content) > 200
            else obj.chunk_content
        )
    
    chunk_content_summary.short_description = "Chunk Content Summary"
