from pathlib import Path
from uuid import uuid4

import hashlib
import requests
from celery import shared_task
from django.conf import settings

from .models import Document, DocumentChunk, DocumentReview, Task, ReviewTask
from common.lctools import data_loader
from common.lctools import llm_tool


MEDIA_ROOT: Path = settings.MEDIA_ROOT


@shared_task
def handle_uploaded_file(file):
    # 创建新的 Task 对象
    task_id = uuid4()
    task = Task.objects.create(id=task_id, status="in_progress")

    # 这里是您处理文件的逻辑
    # ...

    # 更新 Task 状态
    task.status = "completed"
    task.save()


@shared_task
def handle_uploaded_url(url):
    task_id = uuid4()
    task = Task.objects.create(id=task_id, status="in_progress")
    try:
        content = requests.get(url).text
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    except Exception as err:
        print(err)
        task.status = "failed"
        task.message = f"failed to fetch content from {url}"
        task.save()
        return task

    if not Document.objects.filter(id=content_hash).exists():
        file_url = f"documents/{content_hash}.html"
        file_path = MEDIA_ROOT / file_url
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        try:
            Document.objects.create(
                id=content_hash,
                task_id=task_id,
                source=url,
                file_path=file_url,
            )
            task.status = "completed"
        except Exception as err:
            print(err)
            task.status = "failed"
            task.message = str(err)
            task.save()

        task.save()


@shared_task
def process_document_chunks(document_id):
    task = Task.objects.create(status="in_progress")

    if not document_id:
        task.status = "failed"
        task.message = "Document ID is required"
        task.save()
        return

    try:
        document = Document.objects.get(id=document_id)
        DocumentChunk.objects.filter(document=document).delete()

        file_path = MEDIA_ROOT / document.file_path.name
        chunks = data_loader.process_document(file_path.as_posix())
        for i, chunk in enumerate(chunks):
            doc_chunk = DocumentChunk.objects.create(
                document=document,
                chunk_content=chunk.page_content,
                order=i,
            )
            doc_chunk.save()

        task.status = "completed"
    except Exception as e:
        print(e)
        task.status = "failed"
        task.message = str(e)

    task.save()


@shared_task
def review_document_chunks(document_id):
    task = ReviewTask.objects.create(status="in_progress")

    if not document_id:
        task.status = "failed"
        task.message = "Document ID is required"
        task.save()
        return

    try:
        document = Document.objects.get(id=document_id)
        chunks = DocumentChunk.objects.filter(document=document)

        for chunk in chunks:
            summary = llm_tool.run_summary(chunk.chunk_content)
            print(summary)
            review = llm_tool.run_review(chunk.chunk_content)
            print(review)
            doc_review = DocumentReview.objects.create(
                document=document,
                task=task,
                chunk_content=chunk.chunk_content,
                order=chunk.order,
                summary=summary,
                review=review,
            )
            doc_review.save()

        task.status = "completed"
    except Exception as e:
        print(e)
        task.status = "failed"
        task.message = str(e)

    task.save()
