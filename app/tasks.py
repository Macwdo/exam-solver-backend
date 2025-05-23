from celery import shared_task

from app.services.ai_flows import AiFlowsService


@shared_task
def upload_document_task(exam_id: int, file_path: str):
    from app.models import Exam

    exam = Exam.objects.get(id=exam_id)

    service = AiFlowsService(exam, file_path)
    service.run()
