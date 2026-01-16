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