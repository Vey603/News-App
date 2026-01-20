"""Utilidades varias de la Aplicación"""


def clean_text(text: str) -> str:
    # PEP 8: 4 espacios por identación, no tabs
    """Limpia y normaliza en texto."""  # PEP 8: Docstrings en comillas dobles triples
    if not text:
        return ""
    return text.strip().lower()


def process_article_data(raw_data: dict) -> dict:
    """Procesa datos crudos de artículo"""
    return {}


def get_unique_sources(articles):
    return {
        article.get("source").get("name")
        for article in articles
        if article.get("source") and article.get("source").get("name")
    }


def get_articles_by_source(articles: list[dict], source: str) -> list[dict]:
    return list(
        filter(
            lambda article: article["source"]["name"].lower() == source.lower(),
            articles,
        )
    )
