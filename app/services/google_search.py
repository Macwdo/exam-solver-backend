import requests
from django.conf import settings
from pydantic import BaseModel as PydanticBaseModel


class GoogleSearchItem(PydanticBaseModel):
    link: str


class GoogleSearchResponse(PydanticBaseModel):
    items: list[GoogleSearchItem]


class CustomSearchGoogleService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.cx = settings.GOOGLE_CX

    def _search(self, q: str):
        url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.cx}&q={q}"
        response = requests.get(url)
        return response

    def get_search_links(self, q: str):
        response = self._search(q)
        return GoogleSearchResponse(**response.json())
