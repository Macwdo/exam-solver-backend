import logging

from django import forms
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from app.models import Document, Exam
from app.tasks import upload_document_task

logger = logging.getLogger(__name__)


def get_exam(request: HttpRequest, key: str):  # noqa: ARG001
    exam = get_object_or_404(Exam, key=key)
    return JsonResponse(exam.answer if exam.answer else [], safe=False)


def get_exams(request: HttpRequest):  # noqa: ARG001
    exams = list(Exam.objects.all().values("name", "key", "status"))
    return JsonResponse(exams, safe=False)


class CreateDocumentRequest(forms.Form):
    exam_key = forms.CharField()
    file = forms.FileField()
    refetch = forms.BooleanField(required=False)


@csrf_exempt
def upload_document(request: HttpRequest):
    form = CreateDocumentRequest(request.POST, request.FILES)

    form.full_clean()
    data = form.cleaned_data

    if not form.is_valid():
        return JsonResponse({"message": "Invalid form"}, status=status.HTTP_400_BAD_REQUEST)

    exam_key = data["exam_key"]
    exam = Exam.objects.filter(key=exam_key).first()

    if not exam:
        return JsonResponse({"message": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

    file = data["file"]
    document = Document.objects.create(file=file)

    refetch = data["refetch"]
    upload_document_task.delay(exam.id, document.id, refetch)

    return JsonResponse({"message": "Document created successfully"}, status=status.HTTP_201_CREATED)
