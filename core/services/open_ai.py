import openai


class OpenAiService:
    def __init__(self):
        self.client = openai.OpenAI()

    def get_openai_client(self):
        return self.client


service = OpenAiService()
