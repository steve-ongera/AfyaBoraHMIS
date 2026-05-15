"""
AfyaBoraHMIS — main urls.py  (project-level, e.g. afyabora/urls.py)

Mount this in your project's root URL configuration.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # DRF browsable API auth (for development)
    path('api-auth/', include('rest_framework.urls')),

    # All app API routes under /api/v1/
    path('api/v1/', include('core.urls')),          # replace 'core' with your actual app name
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # DRF Swagger / ReDoc docs (optional — install drf-spectacular or drf-yasg)
    try:
        from drf_spectacular.views import (
            SpectacularAPIView,
            SpectacularSwaggerView,
            SpectacularRedocView,
        )
        urlpatterns += [
            path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
            path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]
    except ImportError:
        pass