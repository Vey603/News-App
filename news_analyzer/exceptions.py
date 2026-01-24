"""
Excepciones personalizadas del sistema de noticias.

Este módulo define las excepciones personalizadas utilizadas en la aplicación
de noticias para manejar errores específicos relacionados con APIs externas
y operaciones del sistema.

Jerarquía de excepciones
------------------------
NewsSystemError
    └── APIKeyError

Clases
------
NewsSystemError
    Excepción base para todos los errores del sistema de noticias.
APIKeyError
    Excepción para errores relacionados con claves de API inválidas.

Ejemplos
--------
>>> try:
...     raise APIKeyError("Clave de API inválida")
... except NewsSystemError as e:
...     print(f"Error del sistema: {e}")
Error del sistema: Clave de API inválida
"""


class NewsSystemError(Exception):
    """Error general en la app"""

    pass


class APIKeyError(NewsSystemError):
    """Error cuando la APIKey es inválida"""

    pass
