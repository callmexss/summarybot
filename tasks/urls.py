from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, ReviewTaskViewSet


router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"review-tasks", ReviewTaskViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
