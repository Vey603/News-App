import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def analyzer_articles_whit_ai(articles: list[dict], query: str) -> str:
    """
    Analiza artículos de noticias utilizando un agente de IA de Groq.

    Procesa una lista de artículos de noticias y utiliza el modelo de lenguaje
    LLaMA 3.3 70B a través de la API de Groq para responder preguntas o realizar
    análisis sobre el contenido. Construye un contexto con los primeros 10
    artículos y genera una respuesta concisa en español.

    Parámetros
    ----------
    articles : list[dict]
        Lista de diccionarios donde cada elemento representa un artículo de noticias.
        Cada diccionario debe contener al menos las claves:
        - 'title' (str): Título del artículo
        - 'description' (str): Descripción o resumen del artículo
    query : str
        Pregunta o consulta que se desea realizar sobre los artículos.
        Por ejemplo: "¿Cuál es la tendencia principal?", "Resume los temas principales".

    Retorna
    -------
    str
        Respuesta generada por el modelo de IA en español, basada en el análisis
        de los artículos proporcionados. La función imprime la respuesta pero
        actualmente retorna None implícitamente.

    Excepciones
    -----------
    KeyError
        Si algún artículo en la lista no contiene las claves 'title' o 'description'.
    groq.APIError
        Si hay problemas al comunicarse con la API de Groq.
    groq.AuthenticationError
        Si la API key de Groq no es válida o no está configurada en las
        variables de entorno (API_KEY_GROQ).
    IndexError
        Si la lista de artículos está vacía o la respuesta de la API no contiene
        el formato esperado.

    Ejemplo
    --------
    >>> articulos = [
    ...     {
    ...         'title': 'Avances en IA',
    ...         'description': 'Nuevos modelos de lenguaje superan expectativas...'
    ...     },
    ...     {
    ...         'title': 'Tecnología 2024',
    ...         'description': 'Las principales tendencias tecnológicas del año...'
    ...     }
    ... ]
    >>> analyzer_articles_whit_ai(articulos, "¿Cuál es el tema principal?")
    El tema principal es el avance de la inteligencia artificial y las nuevas
    tecnologías emergentes en 2024.
    """
    client = Groq(
        api_key=os.environ.get("API_KEY_GROQ"),
    )

    context = "\n".join(
        [
            f"Título: {article['title']} - Descripción: {article['description'][:100]}"
            for article in articles[:10]
        ]
    )

    prompt = f"""
        Basandote en estas noticias:
        {context}
        Pregunta: {query}. Responde de forma concisa en español
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)
