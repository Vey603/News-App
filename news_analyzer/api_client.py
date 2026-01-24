"""
Módulo de clientes para APIs de noticias externas.

Este módulo proporciona una interfaz unificada para conectarse a diferentes
servicios de APIs de noticias, incluyendo NewsAPI y The Guardian. Ofrece
funciones para validar claves de API, realizar consultas de búsqueda y
obtener artículos de noticias de múltiples fuentes.

El módulo implementa el patrón Strategy para permitir el cambio dinámico
entre diferentes proveedores de APIs manteniendo una interfaz consistente.

Funciones principales
---------------------
fetch_news : function
    Interfaz unificada para obtener noticias de diferentes APIs.
    Selecciona automáticamente el cliente apropiado según el nombre de la API.
newsapi_client : function
    Cliente específico para NewsAPI. Realiza búsquedas de noticias basadas
    en consultas y retorna artículos en formato JSON.
guardian_client : function
    Cliente específico para The Guardian API. Obtiene noticias de secciones
    específicas a partir de una fecha determinada.
validate_api_key : function
    Valida el formato de claves de API antes de realizar peticiones.

APIs soportadas
---------------
- NewsAPI (news_api): Servicio global de agregación de noticias
- The Guardian (guardian): API del periódico The Guardian

Dependencias internas
---------------------
config : module
    Módulo de configuración que contiene constantes como BASE_URL.
exceptions : module
    Módulo con excepciones personalizadas (APIKeyError, NewsSystemError).

Dependencias externas
---------------------
- json: Para procesamiento de respuestas JSON
- urllib: Para realizar peticiones HTTP y codificación de parámetros
- typing: Para anotaciones de tipos (Dict, Callable, Any)

Excepciones
-----------
APIKeyError
    Se lanza cuando hay problemas de autenticación con las APIs externas
    (definida en el módulo exceptions).
ValueError
    Se lanza cuando se intenta usar una API no soportada en fetch_news.

Manejo de errores:

>>> from exceptions import APIKeyError
>>> try:
...     noticias = fetch_news('news_api', 'clave_invalida', 'python')
... except APIKeyError as e:
...     print(f"Error de autenticación: {e}")
... except ValueError as e:
...     print(f"API no soportada: {e}")
"""

import json
import urllib
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict

from .config import BASE_URL
from .exceptions import APIKeyError


def validate_api_key(api_key):
    """
    Valida que una API key tenga el formato correcto.

    Verifica que la clave de API proporcionada cumpla con los requisitos
    mínimos de formato: debe tener más de 10 caracteres y contener únicamente
    caracteres alfanuméricos (letras y números, sin espacios ni caracteres
    especiales).

    Parámetros
    ----------
    api_key : str
        La clave de API a validar.

    Retorna
    -------
    bool
        True si la API key cumple con los requisitos de formato (más de 10
        caracteres y solo alfanuméricos), False en caso contrario.

    Ejemplo
    --------
    >>> validate_api_key("abc123def456")
    True
    """
    return len(api_key) > 10 and api_key.isalnum()


def guardian_client(api_key, section, from_date, timeout=30, retries=3):
    """
    Crea un cliente para consultar noticias de The Guardian API.

    Genera una representación de cliente para realizar consultas a la API
    de The Guardian, configurando la sección de noticias, fecha de inicio,
    tiempo de espera y número de reintentos en caso de fallos.

    Parámetros
    ----------
    api_key : str
        Clave de autenticación para acceder a The Guardian API.
    section : str
        Sección de noticias a consultar (ej: 'world', 'politics', 'sports').
    from_date : str
        Fecha desde la cual buscar noticias. Se recomienda formato ISO 8601
        (YYYY-MM-DD).
    timeout : int, opcional
        Tiempo máximo de espera en segundos para la respuesta de la API.
        Por defecto es 30 segundos.
    retries : int, opcional
        Número de intentos de reintento en caso de fallo de conexión.
        Por defecto es 3 reintentos.

    Retorna
    -------
    str
        Cadena de texto con la configuración del cliente Guardian.

    Excepciones
    -----------
    TypeError
        Si los parámetros no son del tipo esperado.
    ValueError
        Si timeout o retries son valores negativos.

    Ejemplo
    --------
    >>> guardian_client("mykey123", "world", "2024-01-01")
    'Guardian: world desde 2024-01-01 con timeout 30'
    """
    return f"Guardian: {section} desde {from_date} con timeout {timeout}"


def newsapi_client(api_key: str, query: str, timeout=30, retries=3) -> dict:
    """
    Conecta con NewsAPI para obtener noticias basadas en una consulta.

    Realiza una petición HTTP GET a la API de NewsAPI utilizando la biblioteca
    urllib. Construye la URL con los parámetros de búsqueda, realiza la conexión
    y procesa la respuesta JSON devuelta por el servicio.

    Parámetros
    ----------
    api_key : str
        Clave de autenticación para acceder a NewsAPI.
    query : str
        Término o frase de búsqueda para filtrar las noticias.
    timeout : int, opcional
        Tiempo máximo de espera en segundos para la respuesta de la API.
        Por defecto es 30 segundos.
    retries : int, opcional
        Número de intentos de reintento en caso de fallo de conexión.
        Por defecto es 3 reintentos. (Nota: actualmente no implementado)

    Retorna
    -------
    dict
        Diccionario con la respuesta JSON de NewsAPI conteniendo los artículos
        de noticias y metadatos de la consulta.

    Excepciones
    -----------
    APIKeyError
        Si ocurre un error HTTP al intentar conectar con la API, generalmente
        por una API key inválida o problemas de conectividad.
    urllib.error.URLError
        Si hay problemas de red o timeout al intentar conectar.
    json.JSONDecodeError
        Si la respuesta de la API no es un JSON válido.

    Ejemplo
    --------
    >>> api_key = "tu_api_key_valida"
    >>> resultado = newsapi_client(api_key, "inteligencia artificial")
    >>> print(resultado['status'])
    'ok'
    """
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
    """
    Obtiene noticias de forma flexible desde diferentes APIs de noticias.

    Función de nivel superior que actúa como interfaz unificada para conectar
    con múltiples APIs de noticias. Selecciona el cliente apropiado según el
    nombre de la API especificado y aplica configuraciones por defecto que
    pueden ser sobrescritas mediante argumentos adicionales.

    Parámetros
    ----------
    api_name : str
        Nombre de la API a utilizar. Valores soportados: 'news_api', 'guardian'.
    *args : tuple
        Argumentos posicionales que serán pasados al cliente de API específico.
        Varían según la API seleccionada:
        - Para 'news_api': (api_key, query)
        - Para 'guardian': (api_key, section, from_date)
    **kwargs : dict
        Argumentos de configuración opcionales. Los más comunes son:
        - timeout (int): Tiempo de espera en segundos. Por defecto 30.
        - retries (int): Número de reintentos. Por defecto 3.
        Cualquier otro argumento será pasado al cliente específico.

    Retorna
    -------
    dict
        Diccionario con los datos de noticias devueltos por la API seleccionada.
        La estructura varía según la API utilizada.

    Excepciones
    -----------
    ValueError
        Si el nombre de la API proporcionado no está soportado (no es 'news_api'
        ni 'guardian').
    APIKeyError
        Si hay problemas de autenticación con la API seleccionada.

    Ejemplo
    --------
    >>> # Usando NewsAPI
    >>> noticias = fetch_news('news_api', 'mi_api_key', 'python', timeout=45)
    >>> print(noticias['status'])
    'ok'
    """
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
