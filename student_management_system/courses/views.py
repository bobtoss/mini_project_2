from rest_framework import viewsets
from .models import Course, Enrollment
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin  # Import custom permissions
import logging
logger = logging.getLogger(__name__)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacher | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_student():
            return Course.objects.filter(enrollment__student__user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        if not self.request.user.is_teacher() and not self.request.user.is_admin():
            raise PermissionDenied("You do not have permission to create a course.")
        serializer.save(instructor=self.request.user)

    def list(self, request, *args, **kwargs):
        logger.info("Course list accessed by: %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Course details accessed for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Course creation attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Course update attempt for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Course deletion attempt for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        logger.info("Enrollment list accessed by: %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Enrollment details accessed for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Enrollment creation attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Enrollment update attempt for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Enrollment deletion attempt for course ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)