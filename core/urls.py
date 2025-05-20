from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import get_exam, get_exams, upload_document

urlpatterns = [
    path("admin/", admin.site.urls),
    path("documents/", upload_document, name="create_document"),
    path("exams/<str:key>/", get_exam, name="get_exam"),
    path("exams/", get_exams, name="get_exams"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
