from django.contrib import admin
from .models import Task, ReviewTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "progress", "created_at", "updated_at")


@admin.register(ReviewTask)
class ReviewTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "progress", "created_at", "updated_at")
