import json
import logging

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from app.models import Exam
from app.serializers import CreateDocumentRequest, ExamSerializer, GetPresignedUrlRequest
from app.services.s3_service import S3Service
from app.tasks import upload_document_task

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_exam(request: Request, pk: int):  # noqa: ARG001
    exam = get_object_or_404(Exam, pk=pk)
    serializer = ExamSerializer(exam)

    return Response(serializer.data)


@api_view(["GET"])
def get_exams(request: Request):  # noqa: ARG001
    exams = Exam.objects.all()
    serializer = ExamSerializer(exams, many=True)

    return Response(serializer.data)


@csrf_exempt
def upload_document(request: HttpRequest, pk: int):
    data = json.loads(request.body)

    serializer = CreateDocumentRequest(data=data)
    serializer.is_valid(raise_exception=True)

    upload_document_task.delay(pk, **serializer.validated_data)

    return JsonResponse({"message": "Document created successfully"}, status=status.HTTP_201_CREATED)


@csrf_exempt
def get_presigned_url(request: HttpRequest):
    data = json.loads(request.body)

    serializer = GetPresignedUrlRequest(data=data)
    serializer.is_valid(raise_exception=True)

    service = S3Service()

    presigned_data = service.generate_presigned_url(**serializer.validated_data)

    return JsonResponse(presigned_data, safe=False)
