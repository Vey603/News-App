"""Sistema de análisis de noticias con APIs múltiples"""

from news_analyzer.api_client import fetch_news
from news_analyzer.config import API_KEY_NEWSAPI
from news_analyzer.exceptions import APIKeyError
from news_analyzer.openai import analyzer_articles_whit_ai


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
    analyzer_articles_whit_ai(
        response_data["articles"], "Que piensas acerca de estos articulos?"
    )
# sources_set = get_unique_sources(response_data["articles"])
# for index, source in enumerate(sources_set):
#     print(f"No: {index} -- {source}")

# print("===")

# for article in response_data["articles"]:
#     print(article["title"])

# print("===")

# github_articles = get_articles_by_source(response_data["articles"], "Github.com")
# for github_article in github_articles:
#     print(github_article["title"])

# print("===")

# articles = list(map(get_reading_time, response_data["articles"]))
# for article in articles:
#     print(
#         f"Título: {article['title']} -- Tiempo de lectura: {article['reading_time']}"
#     )
