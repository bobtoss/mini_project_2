from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
from django_filters import rest_framework as filters
import logging

from student_management_system.settings import CACHE_TTL

logger = logging.getLogger(__name__)


class StudentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name', 'email']  # Fields to filter by


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.DjangoFilterBackend]  # Enable filtering
    filterset_class = StudentFilter  # Use the custom filter class

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
        student_id = kwargs['pk']
        cache_key = f"student_profile_{student_id}"
        logger.info("Student details accessed for student ID: %s by: %s", kwargs['pk'], request.user)
        student_data = cache.get(cache_key)
        if not student_data:
            # If not cached, query the database and cache the result
            student = self.get_object()
            serializer = StudentSerializer(student)
            student_data = serializer.data
            cache.set(cache_key, student_data, timeout=CACHE_TTL)
        else:
            # If cached, use the cached data
            student_data = cache.get(cache_key)

        return Response(student_data)

    def create(self, request, *args, **kwargs):
        logger.info("Student creation attempt by: %s", request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        student_id = kwargs['pk']
        cache_key = f"student_profile_{student_id}"
        cache.delete(cache_key)
        logger.info("Student update attempt for student ID: %s by: %s", kwargs['pk'], request.user)
        return response

    def destroy(self, request, *args, **kwargs):
        logger.warning("Student deletion attempt for student ID: %s by: %s", kwargs['pk'], request.user)
        return super().destroy(request, *args, **kwargs)
