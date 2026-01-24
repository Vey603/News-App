"""Utilidades varias de la Aplicación"""


def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.strip().lower()


def process_article_data(raw_data: dict) -> dict:
    return {}


def get_unique_sources(articles):
    """
    Extrae los nombres únicos de fuentes de noticias de una lista de artículos.

    Recorre una lista de artículos y recopila todos los nombres de fuentes
    únicos, eliminando duplicados. Maneja de forma segura artículos que no
    tengan información de fuente o donde la fuente sea None.

    Parámetros
    ----------
    articles : list[dict]
        Lista de diccionarios donde cada elemento representa un artículo.
        Cada artículo debe tener potencialmente una estructura:
        {'source': {'name': 'Nombre de la fuente', ...}, ...}

    Retorna
    -------
    set
        Conjunto (set) con los nombres únicos de las fuentes encontradas.
        Los artículos sin fuente o con fuente None son ignorados.

    Ejemplo
    --------
    >>> articulos = [
    ...     {'source': {'name': 'BBC News'}, 'title': 'Noticia 1'},
    ...     {'source': {'name': 'CNN'}, 'title': 'Noticia 2'},
    ...     {'source': {'name': 'BBC News'}, 'title': 'Noticia 3'},
    ...     {'source': None, 'title': 'Noticia 4'}
    ... ]
    >>> get_unique_sources(articulos)
    {'BBC News', 'CNN'}
    """
    return {
        article.get("source").get("name")
        for article in articles
        if article.get("source") and article.get("source").get("name")
    }


def get_articles_by_source(articles: list[dict], source: str) -> list[dict]:
    """
    Filtra artículos por nombre de fuente específica.

    Busca y retorna todos los artículos que provienen de una fuente de noticias
    específica. La comparación se realiza de forma insensible a mayúsculas/minúsculas
    para mayor flexibilidad.

    Parámetros
    ----------
    articles : list[dict]
        Lista de diccionarios donde cada elemento representa un artículo.
        Cada artículo debe tener la estructura:
        {'source': {'name': 'Nombre de la fuente'}, ...}
    source : str
        Nombre de la fuente de noticias por la cual filtrar. La comparación
        no es sensible a mayúsculas/minúsculas.

    Retorna
    -------
    list[dict]
        Lista con los artículos que coinciden con la fuente especificada.
        Retorna lista vacía si no hay coincidencias.

    Excepciones
    -----------
    KeyError
        Si algún artículo no tiene la estructura esperada con las claves
        'source' y 'name'.

    Ejemplos
    --------
    >>> articulos = [
    ...     {'source': {'name': 'BBC News'}, 'title': 'Noticia BBC 1'},
    ...     {'source': {'name': 'CNN'}, 'title': 'Noticia CNN'},
    ...     {'source': {'name': 'BBC News'}, 'title': 'Noticia BBC 2'}
    ... ]
    >>> bbc_articles = get_articles_by_source(articulos, 'BBC News')
    >>> len(bbc_articles)
    2
    """
    return list(
        filter(
            lambda article: article["source"]["name"].lower() == source.lower(),
            articles,
        )
    )


def get_reading_time(article: dict) -> dict:
    """
    Calcula y agrega el tiempo estimado de lectura a un artículo.

    Estima el tiempo de lectura de un artículo basándose en la longitud de su
    contenido, usando una velocidad de lectura promedio de 200 caracteres por
    minuto. Modifica el diccionario del artículo agregando el campo 'reading_time'.

    Parámetros
    ----------
    article : dict
        Diccionario que representa un artículo de noticias. Debe contener
        la clave 'content' con el texto completo del artículo como string.

    Retorna
    -------
    dict
        El mismo diccionario del artículo con un nuevo campo 'reading_time'
        que contiene el tiempo estimado de lectura en minutos (entero).

    Excepciones
    -----------
    KeyError
        Si el artículo no contiene la clave 'content'.
    TypeError
        Si el contenido no es una cadena de texto o no soporta len().

    Ejemplos
    --------
    >>> articulo = {
    ...     'title': 'Noticia importante',
    ...     'content': 'A' * 500  # 500 caracteres
    ... }
    >>> resultado = get_reading_time(articulo)
    >>> resultado['reading_time']
    3
    """
    minutes = len(article["content"]) // 200 + 1
    article["reading_time"] = minutes
    return article
