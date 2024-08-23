from datetime import datetime
from typing_extensions import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.api.forms.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    GroupAnswerList,
)
from src.api.forms.service import FormService
from src.api.forms.repository import FormRepository
from src.api.topics.repository import TopicRepository

from src.api.exceptions import (
    EntityNotFound,
    Duplicated,
    ServerError,
)
from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/forms", tags=["Forms"])


@router.post(
    "/answers",
    description="This endpoint creates topic preferences answers for sender\
        and students from its group if it belongs to one.",
    response_model=FormPreferencesList,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successfully added topic preferences answers."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happend inside the backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_answers(
    answers: FormPreferencesRequest, session: Annotated[Session, Depends(get_db)]
):
    try:
        service = FormService(FormRepository(session))
        return service.add_answers(answers)
    except (Duplicated, EntityNotFound) as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/answers",
    description="This endpoint return all topic preferences answers grouped by answer \
        id.",
    response_model=GroupAnswerList,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully get all answers grouped by answer id."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_answers(session: Annotated[Session, Depends(get_db)]):
    try:
        service = FormService(FormRepository(session))
        return service.get_answers(TopicRepository(session))
    except Exception as e:
        logger.error("Could not get all the answers from the db")
        raise ServerError(message=str(e))


@router.delete(
    "/answers/{answer_id}",
    description="This endpoint deletes answers by answer id.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully deleted answers by answer id."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_answer(
    answer_id: datetime, session: Annotated[Session, Depends(get_db)]
):
    try:
        service = FormService(FormRepository(session))
        return service.delete_answers_by_answer_id(answer_id)
    except EntityNotFound as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))
