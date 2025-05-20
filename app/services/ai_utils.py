import json
import os

from langchain_community.document_loaders import BSHTMLLoader
from langchain_core.messages import AIMessage


class AiUtilsService:
    def transform_html_into_txt(self, html_file: str, chunk_size: int, chunk_overlap: int):
        chunks = self.transform_html_into_chunks(html_file, chunk_size, chunk_overlap)

        string = ""
        for chunk in chunks:
            string += chunk.page_content

        string = string.strip()
        return string

    def transform_html_into_chunks(self, html_file: str, chunk_size: int, chunk_overlap: int):
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        loader = BSHTMLLoader(html_file)
        documents = loader.lazy_load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(documents)

        return chunks

    def clean_extracted_text(self, text: str):
        text = text.replace("\n", " ").split(" ")
        text = [word for word in text if word]
        text = " ".join(text)
        return text

    def read_file(self, prompt_file: str):
        with open(prompt_file, encoding="utf-8") as f:
            return f.read()

    def write_file(self, file_path: str, content: str):
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def send_to_llm(self, prompt: str, **prompt_args) -> AIMessage:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai.chat_models import ChatOpenAI

        llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)
        output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_template(prompt)

        formatted_prompt = prompt.format(**prompt_args)
        response = llm.invoke(formatted_prompt)

        return output_parser.parse(response)

    def parse_json(self, result: str):
        json_string = result.content.strip("`").replace("json", "").strip()
        json_data = json.loads(json_string)
        return json_data
