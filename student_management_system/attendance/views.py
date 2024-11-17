from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
import logging
logger = logging.getLogger(__name__)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
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
            return Attendance.objects.filter(student__user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        if not self.request.user.is_teacher() and not self.request.user.is_admin():
            raise PermissionDenied("You do not have permission to mark attendance.")
        serializer.save()

    def list(self, request, *args, **kwargs):
        logger.info("Attendance list accessed by: %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Attendance details accessed for attendance ID: %s by: %s", kwargs['pk'], request.user)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Attendance marking attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Attendance update attempt for attendance ID: %s by: %s", kwargs['pk'], request.user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Attendance deletion attempt for attendance ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)