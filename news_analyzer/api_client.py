"""Módulo para interactuar con APIs"""

import json, urllib, urllib.parse, urllib.request
from typing import Callable

from .config import BASE_URL
from .exceptions import APIKeyError

def validate_api_key(api_key):
    """Valida que la API key tenga formato correcto."""
    return len(api_key) > 10 and api_key.isalnum()


def guardian_client(api_key, section, from_date, timeout=30, retries=3):
    return f"Guardian: {section} desde {from_date} con timeout {timeout}"


def newsapi_client(api_key: str, query: str, timeout=30, retries=3) -> dict:
    """API NewsAPI. Función para conectarse a la API y obtener las noticias"""
    query_string: str = urllib.parse.urlencode(
        {"q": query, "apiKey": api_key}
    )  # Formatea la cadena de parámetros a URL
    url: str = f"{BASE_URL}?{query_string}"  # Une la URL base con la cadena de parámetros formateada
    try:
        with urllib.request.urlopen(
            url, timeout=timeout
        ) as response:  # Abre la URL y realiza GET. La respuesta la guarda es response
            data = response.read().decode(
                "utf-8"
            )  # Lee todos los datos de response y lo convierte en una cadena de texto JSON
            return json.loads(data)  # Convierte la cadena JSON en un objeto de Python
    except urllib.error.HTTPError:
        raise APIKeyError("Ocurrió un error, no se pudo conectar con la API.")


def fetch_news(api_name: str, *args, **kwargs) -> dict:
    """Función flexible para conectar con la API"""

    if api_name not in ("news_api", "guardian"):
        raise ValueError(f"Error. API '{api_name}' no soportada.")

        
    base_config = {
        "timeout": 30,
        "retries": 3,
    }

    config = {**base_config, **kwargs}

    api_clients: Dict[str, Callable[..., Any]] = {
        "news_api": newsapi_client,
        "guardian": guardian_client,
    }

    client = api_clients[api_name]
    return client(*args, **config)