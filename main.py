# def ejemplo(api_key, *args):
#     print(f"API Key: {api_key}")
#     print(f"args: {args}")
#     print(f"Type args: {type(args)}")
#     print("=====")


# def suma_numeros(*args):
#     return sum([x for x in args if isinstance(x, (int, float))])


# # ejemplo("API_KEY_VALUE", "Este", "parametro", "acá")
# # ejemplo("API_KEY_VALUE", "Hola", "Mundo")
# # # ejemplo() Error, se espera el parámetro api_key
# # print(suma_numeros(4, 1, 5, 6))


# def ejemplo_kwargs(**kwargs):
#     print(f"Type: {type(kwargs)}")
#     print(f"Kwargs: {kwargs}")
#     print("====")


# ejemplo_kwargs(
#     api_key="beta_newsAPI",
#     query="Noticias de Python",
#     timeout=30,
#     retries=3,
# )
# ejemplo_kwargs(
#     api_key="beta_guardian",
#     section="Sports",
#     from_date="2020-10-20",
#     timeout=30,
#     retries=3,
# )

# main.py - Todo el código en un archivo
import json  # Manipulación de datos en formato JSON
import os
import urllib.parse  # Manipulación y formateo de URLs
import urllib.request  # Peticiones HTTP (GET/POST)
from typing import Any, Callable, Dict

from dotenv import load_dotenv

load_dotenv()

"""
Sistema de análisis de noticias con APIs múltiples.
"""

# PEP 8: Configuración centralizada - constantes en MAYÚSCULAS con guines bajos
API_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_LANGUAGE = "es"  # PEP 8: Comillas dobles para strings
API_KEY_NEWSAPI = os.getenv("API_KEY_NEWSAPI")
BASE_URL: str = "https://newsapi.org/v2/everything"  # Parte inicial de la URL (Sin parámetros de Consulta)


class NewsSystemError(Exception):
    """Error general en la app"""

    pass


class APIKeyError(NewsSystemError):
    """Error cuando la APIKey es inválida"""

    pass


# PEP 8: Utilidades comunes del proyecto - funcione en snake_case
def clean_text(text):
    # PEP 8: 4 espacios por identación, no tabs
    """Limpia y normaliza en texto."""  # PEP 8: Docstrings en comillas dobles triples
    if not text:
        return ""
    return text.strip().lower()


# PEP 8: Doble líneas en blanco entre funciones para separar lógicamente
def validate_api_key(api_key):
    """Valida que la API key tenga formato correcto."""
    return len(api_key) > 10 and api_key.isalnum()


# PEP 8: Funciones principales - agrupadas después de las utilidades
def fetch_news_from_api(api_name, query):
    """Obtiene noticias de una API específica."""
    pass


def process_article_data(raw_data):
    """Procesa datos crudos de artículo"""
    pass


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


def guardian_client(api_key, section, from_date, timeout=30, retries=3):
    return f"Guardian: {section} desde {from_date} con timeout {timeout}"


def fetch_news(api_name: str, *args, **kwargs) -> dict:
    """Función flexible para conectar con la API"""
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


response_data: dict | None = None
try:
    response_data = fetch_news("news_api", api_key=API_KEY_NEWSAPI, query="Python")
except APIKeyError as e:
    print(f"{e}")

if response_data:
    for article in response_data["articles"]:
        print(article["title"])
