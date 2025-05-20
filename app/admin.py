from django.contrib import admin

from .models import Document, Exam


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at", "updated_at")
    search_fields = ("file",)
    list_filter = ("created_at",)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
