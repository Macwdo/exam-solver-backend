import logging

from app.models import Document, Exam
from app.services.ai_utils import AiUtilsService
from app.services.answer_flow import AnswerFlow
from app.services.questions_flow import QuestionsFlow
from app.utils import create_temp_file

logger = logging.getLogger(__name__)


class NotExamException(Exception):
    pass


class AiFlowsService:
    def __init__(self):
        self.questions_flow = QuestionsFlow()
        self.answer_flow = AnswerFlow()
        self.ai_utils_service = AiUtilsService()

    def run(self, exam: Exam, document: Document, refetch: bool):
        logger.info(f"Running exam {exam.name}")

        should_fetch_responses = exam.status in [Exam.Status.COMPLETED, Exam.Status.PROCESSING]
        if should_fetch_responses and not refetch:
            logger.info(f"Exam {exam.name} already has answers")
            logger.info(f"Finished exam {exam.name}")
            return

        try:
            exam.status = Exam.Status.PROCESSING
            exam.save()

            questions = self.get_questions(exam, document)
            answers = self.get_answers(exam, questions)

            exam.status = Exam.Status.COMPLETED
            exam.answer = [answer.model_dump() for answer in answers]
            exam.save()

        except NotExamException:
            logger.info(f"Document {document.file.name} is not an exam")
            exam.status = Exam.Status.FAILED
            exam.save()

        except Exception as e:
            logger.error(f"Error running exam {exam.name}: {e}")
            exam.status = Exam.Status.FAILED
            exam.save()

    def get_questions(self, exam: Exam, document: Document):
        with create_temp_file(".html") as tmp_file:
            html = document.file.read()
            with open(tmp_file, "wb") as f:
                f.write(html)

            questions = self.questions_flow.get_questions(tmp_file, exam)

        return questions

    def get_answers(
        self,
        exam: Exam,
        questions: list[Exam.StructuredQuestion],
    ) -> list[Exam.StructuredQuestionWithAnswer]:
        answers = []
        for question in questions:
            answer = self.answer_flow.get_answer_from_internet(exam, question)

            if isinstance(answer, Exam.StructuredQuestionWithAnswer):
                answers.append(answer)

            elif isinstance(answer, str):
                answer = self.answer_flow.get_answer_from_context(exam, question)
                answers.append(answer)

        return answers
