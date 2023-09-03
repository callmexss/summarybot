from pathlib import Path
from django.db import models
from tasks.models import ReviewTask, Task


class Document(models.Model):
    id = models.CharField(
        max_length=64, primary_key=True
    )  # This will store the hash value
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    file_path = models.FileField(
        upload_to="documents/"
    )  # This assumes you've configured your MEDIA settings
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=200)

    def __str__(self):
        return Path(self.source).stem


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document, related_name="chunks", on_delete=models.CASCADE
    )
    chunk_content = models.TextField()
    order = models.IntegerField()


class DocumentReview(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    task = models.ForeignKey(ReviewTask, null=True, on_delete=models.SET_NULL)
    chunk_content = models.TextField()
    order = models.IntegerField()
    summary = models.TextField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
