# =============================================================================
# IMPORTANTE: Este modulo de Python incluye todas las dependencias.
# No esta destinado a contener clases; en su lugar, debe incluir funciones
# para ser importadas.
# Asegurate de seguir esta estructura para mantener la consistencia
# =============================================================================


from src.config.config import api_config
from src.core.email_client import SendGridEmailClient


def get_email_sender():
    email_client = SendGridEmailClient(api_key=api_config.email_key)
    yield email_client
