from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from datetime import datetime

from src.api.form.schemas import GroupFormRequest, GroupFormResponse
from src.api.form.service import FormService
from src.api.form.repository import FormRepository
from src.api.form.exceptions import (
    StudentNotFound,
    TopicNotFound,
    DuplicatedAnswer,
    GroupIdNotFound,
)

from src.config.database import get_db

router = APIRouter(prefix="/forms", tags=["Forms"])


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
async def add_group_form(
    group_form: GroupFormRequest, session: Annotated[Session, Depends(get_db)]
):
    try:
        service = FormService(FormRepository(session))
        return service.add_group_form(group_form)
    except (StudentNotFound, TopicNotFound, DuplicatedAnswer) as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {err}",
        )


@router.delete(
    "/groups/{group_id}",
    description="This endpoint deletes answers by group id.",
    responses={
        status.HTTP_200_OK: {"description": "Successfully deleted answers by group id"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_group_form(
    group_id: datetime, session: Annotated[Session, Depends(get_db)]
):
    try:
        service = FormService(FormRepository(session))
        return service.delete_group_form_by_group_id(group_id)
    except GroupIdNotFound as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err,
        )
