import logging
from uuid import uuid4

from app.models import Exam
from app.services.ai_utils import AiUtilsService
from app.services.answer_flow import AnswerFlow
from app.services.questions_flow import QuestionsFlow
from app.services.selenium_scrapper import SeleniumScrapperService
from app.services.storage import StorageManager

logger = logging.getLogger(__name__)


class NotExamException(Exception):
    pass


class AiFlowsService:
    def __init__(self, exam: Exam, file: str):
        self.exam = exam
        self.file = file
        self.random_file_name = uuid4().hex + ".html"

        self._questions_flow = QuestionsFlow()
        self._answer_flow = AnswerFlow()
        self._ai_utils_service = AiUtilsService()
        self._storage_manager = StorageManager()

    def run(self):
        exam = self.exam

        logger.info(f"Running exam {exam.name}")

        should_fetch_responses = exam.status in [Exam.Status.COMPLETED, Exam.Status.PROCESSING]
        if should_fetch_responses:
            logger.info(f"Exam {exam.name} already has answers")
            logger.info(f"Finished exam {exam.name}")
            return

        try:
            exam.status = Exam.Status.PROCESSING
            exam.save()

            questions = self.get_questions()
            answers = self.get_answers(questions)

            exam.status = Exam.Status.COMPLETED
            exam.answer = [answer.model_dump() for answer in answers]
            exam.save()

        except NotExamException:
            logger.info(f"Document {self.file} is not an exam")
            exam.status = Exam.Status.FAILED
            exam.save()

        except Exception as e:
            logger.error(f"Error running exam {self.file}: {e}")
            exam.status = Exam.Status.FAILED
            exam.save()

        finally:
            self._storage_manager.cleanup()

    def get_questions(self):
        self._storage_manager.write_file(self.random_file_name, self.file)
        self._storage_manager.track_file(self.random_file_name)

        questions = self._questions_flow.get_questions(self.random_file_name, self.exam)

        return questions

    def get_answers(
        self,
        questions: list[Exam.StructuredQuestion],
    ) -> list[Exam.StructuredQuestionWithAnswer]:
        logger.info(f"Getting answers for {self.exam.name}")

        answers = []
        selenium_scrapper_service = SeleniumScrapperService()
        for index, question in enumerate(questions, 1):
            answer = self._answer_flow.get_answer_from_gpt_search_model(self.exam, question)

            if isinstance(answer, Exam.StructuredQuestionWithAnswer):
                logger.info(f"Answer found for question {index}")

                answers.append(answer)

            elif isinstance(answer, str):
                logger.info(f"Answer not found for question {index}")

                answer = self._answer_flow.get_answer_from_context(answer, question)
                answers.append(answer)

        selenium_scrapper_service.stop()
        logger.info(f"Got {len(answers)} answers for {self.exam.name}")

        return answers
