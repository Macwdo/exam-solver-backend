from celery import shared_task

from app.services.ai_flows import AiFlowsService


@shared_task()
def upload_document_task(exam_id: int, document_id: int, refetch: bool):
    from app.models import Document, Exam

    exam = Exam.objects.get(id=exam_id)
    document = Document.objects.get(id=document_id)

    service = AiFlowsService()

    service.run(exam, document, refetch)
