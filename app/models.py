from __future__ import annotations

from django.db import models
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Document(BaseModel):
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return f"Document(id={self.id}, file={self.file.name})"


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
    key = models.CharField(max_length=3, db_index=True, unique=True)

    answer = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)

    def __str__(self):
        return f"Exam(id={self.id}, name={self.name}, key={self.key})"
