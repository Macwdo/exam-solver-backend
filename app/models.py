from __future__ import annotations

from django.db import models
from django.utils import timezone
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Exam(BaseModel):
    class Status(models.TextChoices):
        NOT_STARTED = "not_started"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    class Alternative(PydanticBaseModel):
        letter: str
        text: str

    class StructuredQuestion(PydanticBaseModel):
        number: int
        question: str
        alternatives: list[Exam.Alternative]

    class StructuredQuestionWithAnswer(StructuredQuestion):
        answer: Exam.Alternative | None

    name = models.CharField(max_length=255)
    answer = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    date = models.DateTimeField(null=True, blank=True)
    by_pass_is_blocked = models.BooleanField(default=False)
    input_document = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Exam(id={self.id}, name={self.name})"

    @property
    def is_blocked(self):
        if not self.date:
            return False

        if self.by_pass_is_blocked:
            return False

        return timezone.now() < self.date
