"""Configuración de la Aplicación"""

import os

from dotenv import load_dotenv

load_dotenv()

API_KEY_NEWSAPI = os.getenv("API_KEY_NEWSAPI")
BASE_URL = "https://newsapi.org/v2/everything"  # Parte inicial de la URL (Sin parámetros de Consulta)