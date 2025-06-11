from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import get_exams, upload_document

urlpatterns = [
    path("upload-documents/<int:pk>/", upload_document, name="create_document"),
    path("exams/", get_exams, name="get_exams"),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
