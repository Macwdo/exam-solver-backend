from django.contrib import admin

from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "is_blocked",
        "by_pass_is_blocked",
        "date",
    )
    search_fields = ("name",)
    list_filter = ("created_at", "status")
    ordering = ("date", "-id")
