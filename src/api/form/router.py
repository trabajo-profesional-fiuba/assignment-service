from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from src.api.form.schemas import GroupFormRequest, GroupFormResponse
from src.api.form.service import FormService
from src.api.form.repository import FormRepository
from src.api.form.exceptions import UidDuplicated, TopicNotFound

from src.config.database import get_db

router = APIRouter(prefix="/forms", tags=["forms"])


@router.post(
    "/groups",
    description="This endpoint creates a new topic preferences answer of email sender\
        and students from its group if it belongs to one.",
    response_description="List of created topic preferences answers of email sender\
        and students from its group if it belongs to one.",
    response_model=list[GroupFormResponse],
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successfully added topic preferences"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_topic_preferences(
    group_form: GroupFormRequest, session: Annotated[Session, Depends(get_db)]
):
    try:
        service = FormService(FormRepository(session))
        res = service.add_group_submition(group_form)
        return res
    except UidDuplicated as uid:
        raise HTTPException(
            status_code=409,
            detail=f"Student uid '{uid}' already exists.",
        )
    except TopicNotFound as topic:
        raise HTTPException(
            status_code=409,
            detail=f"Topic '{topic.name}', '' not found.",
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")
