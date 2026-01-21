import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def analyzer_articles_whit_ai(articles: list[dict], query: str) -> str:
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
