# =============================================================================
# IMPORTANT: This Python module includes all dependencies related to groups.
# It is not intended to contain classes; instead, it should include functions
# to be imported. Ensure to follow this structure to maintain consistency and
# functionality across projects.
# =============================================================================


from src.core.email_client import SendGridEmailClient
from src.config.config import api_config


def get_email_sender():
    email_client = SendGridEmailClient(api_key=api_config.email_key)
    yield email_client
