from rest_framework import viewsets

from .models import Task, ReviewTask
from .serializers import TaskSerializer, ReviewTaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ReviewTaskViewSet(viewsets.ModelViewSet):
    queryset = ReviewTask.objects.all()
    serializer_class = ReviewTaskSerializer
