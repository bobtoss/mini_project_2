from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserDetailView, RegisterView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),  # use this endpoint to get jwt token
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
]
