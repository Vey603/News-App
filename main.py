"""Sistema de análisis de noticias con APIs múltiples"""

from news_analyzer.config import API_KEY_NEWSAPI
from news_analyzer.exceptions import APIKeyError
from news_analyzer.api_client import fetch_news

from dotenv import load_dotenv

load_dotenv()


# PEP 8: Funciones principales - agrupadas después de las utilidades
def fetch_news_from_api(api_name, query):
    """Obtiene noticias de una API específica."""
    pass


response_data: dict | None = None
try:
    response_data = fetch_news("news_api", api_key=API_KEY_NEWSAPI, query="Python")
except APIKeyError as e:
    print(f"{e}")

if response_data:
    for article in response_data["articles"]:
        print(article["title"])
