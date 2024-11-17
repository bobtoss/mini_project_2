from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
import logging
logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsStudent | IsTeacher | IsAdmin]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        logger.info("Student list accessed by: %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Student details accessed for student ID: %s by: %s", kwargs['pk'], request.user)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Student creation attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Student update attempt for student ID: %s by: %s", kwargs['pk'], request.user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Student deletion attempt for student ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)
