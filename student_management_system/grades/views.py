from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
import logging
logger = logging.getLogger(__name__)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsStudent | IsTeacher | IsAdmin]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacher | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_student():
            return Grade.objects.filter(student__user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        if not self.request.user.is_teacher() and not self.request.user.is_admin():
            raise PermissionDenied("You do not have permission to assign grades.")
        serializer.save(teacher=self.request.user)

    def list(self, request, *args, **kwargs):
        logger.info("Grade list accessed by: %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Grade details accessed for grade ID: %s by: %s", kwargs['pk'], request.user)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Grade assignment attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Grade update attempt for grade ID: %s by: %s", kwargs['pk'], request.user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Grade deletion attempt for grade ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)