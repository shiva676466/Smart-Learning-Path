"""Smart Learning Path Generator - Root URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('progress/', include('progress.urls')),
    path('api/', include('roadmap.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
