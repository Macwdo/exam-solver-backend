import logging

from pydantic import BaseModel as PydanticBaseModel

from app.models import Exam
from app.services.ai_utils import AiUtilsService
from app.services.google_search import CustomSearchGoogleService
from app.services.selenium_scrapper import SeleniumScrapperService
from app.utils import create_temp_file, time_it

logger = logging.getLogger(__name__)


class AnswerResponse(PydanticBaseModel):
    found: bool
    answer: Exam.Alternative | None
    context: str
    accuracy: int


class AnswerFlow:
    ANSWER_PROMPT = "app/prompts/answer.txt"
    ANSWER_FROM_CONTEXT_PROMPT = "app/prompts/answer_from_context.txt"

    def __init__(self):
        self.ai_utils_service = AiUtilsService()
        self.google_search_service = CustomSearchGoogleService()

    @time_it
    def get_answer_from_internet(
        self,
        exam: Exam,
        question: Exam.StructuredQuestion,
        selenium_scrapper_service: SeleniumScrapperService,
    ) -> Exam.StructuredQuestionWithAnswer | str:
        prompt = self.ai_utils_service.read_file(AnswerFlow.ANSWER_PROMPT)

        logger.info(f"Getting search links for {question.question}")
        search_links = self.google_search_service.get_search_links(question.question)

        first_three_items = search_links.items[:3]
        for item in first_three_items:
            link = item.link

            logger.info(f"Getting HTML for {link}")
            html = selenium_scrapper_service.get_html(link)
            chunks = self._get_chunks(html)

            context = ""
            for chunk in chunks:
                chunk_cleaned_text = self.ai_utils_service.clean_extracted_text(chunk.page_content)

                logger.info(f"Sending prompt to LLM for {link}")
                result = self.ai_utils_service.send_to_llm(
                    prompt,
                    subject_input=exam.name,
                    question_input=question.question,
                    alternatives_input=question.alternatives,
                    context_input=context,
                    document_input=chunk_cleaned_text,
                )

                json_parsed = self.ai_utils_service.parse_json(result)
                answer_response = AnswerResponse(**json_parsed)
                if answer_response.accuracy > 60 and answer_response.found:
                    return Exam.StructuredQuestionWithAnswer(
                        **question.model_dump(),
                        answer=answer_response.answer,
                    )

        return answer_response.context

    def _get_chunks(self, html: str):
        with create_temp_file(".html") as temp_file:
            with open(temp_file, "w") as f:
                f.write(html)

            chunks = self.ai_utils_service.transform_html_into_chunks(temp_file, 3000, 200)

            return chunks

    def get_answer_from_context(self, context: str, question: Exam.StructuredQuestion):
        prompt = self.ai_utils_service.read_file(AnswerFlow.ANSWER_FROM_CONTEXT_PROMPT)
        result = self.ai_utils_service.send_to_llm(
            prompt,
            question_input=question.question,
            context_input=context,
            alternatives_input=question.alternatives,
        )

        json_parsed = self.ai_utils_service.parse_json(result)
        answer_response = Exam.StructuredQuestionWithAnswer(**json_parsed)

        return answer_response
