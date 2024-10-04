# =============================================================================
# IMPORTANT: This Python module includes all dependencies related to groups.
# It is not intended to contain classes; instead, it should include functions
# to be imported. Ensure to follow this structure to maintain consistency and
# functionality across projects.
# =============================================================================


from fastapi import BackgroundTasks

from src.api.groups.repository import GroupRepository
from src.core.email_client import SendGridEmailClient
from src.config.config import api_config


def get_email_sender(
    background_tasks: BackgroundTasks,
    group_id: int,
    group_repository: GroupRepository,
    subject: str = "Asunto",
    body: str = "Cuerpo",
):
    email_client = SendGridEmailClient(api_key=api_config.email_key)
    background_tasks.add_task(email_client.send_email,'alejovillores@gmail.com','Test','body')
