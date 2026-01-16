"""Excepciones personalizadas de la Aplicación"""


class NewsSystemError(Exception):
    """Error general en la app"""

    pass


class APIKeyError(NewsSystemError):
    """Error cuando la APIKey es inválida"""

    pass