import logging

from pydantic import BaseModel as PydanticBaseModel

from app.models import Exam
from app.services.ai_utils import AiUtilsService
from app.utils import time_it

logger = logging.getLogger(__name__)


class QuestionsValidation(PydanticBaseModel):
    valid: bool
    questions: list[Exam.StructuredQuestion]


class QuestionsFlow:
    QUESTIONS_PROMPT = "app/prompts/questions.txt"

    def __init__(self):
        self.ai_utils_service = AiUtilsService()

    @time_it
    def get_questions(self, file_path: str, exam: Exam):
        from app.services.ai_flows import NotExamException

        text = self.ai_utils_service.transform_html_into_txt(file_path, 3000, 200)
        prompt = self.ai_utils_service.read_file(QuestionsFlow.QUESTIONS_PROMPT)
        result = self.ai_utils_service.send_to_llm(
            prompt,
            text=text,
            subject=exam.name,
        )

        json_parsed = self.ai_utils_service.parse_json(result)
        question_reponse = QuestionsValidation(**json_parsed)
        if not question_reponse.valid:
            raise NotExamException

        return question_reponse.questions
