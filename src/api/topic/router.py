from fastapi import APIRouter, status, Depends, UploadFile
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session


from src.api.topic.schemas import (
    TopicResponse,
)
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.config.database import get_db
from src.api.topic.exceptions import (
    TopicAlreadyExist,
    InvalidMediaType,
    InvalidTopicCsv,
)

router = APIRouter(prefix="/topics", tags=["topics"])


@router.post(
    "/upload",
    response_model=list[TopicResponse],
    description="Creates a list of topics based on a csv file",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added topics."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Columns don't match with expected."
        },
        status.HTTP_409_CONFLICT: {"description": "Topic already exists."},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Invalid file type."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error."
        },
    },
)
async def upload_csv_file(
    file: UploadFile,
    session: Annotated[Session, Depends(get_db)],
):
    try:
        if file.content_type != "text/csv":
            raise InvalidMediaType("CSV file must be provided.")
        content = (await file.read()).decode("utf-8")
        service = TopicService(TopicRepository(session))
        return service.create_topics_from_string(content)
    except (TopicAlreadyExist, InvalidMediaType, InvalidTopicCsv) as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {err}",
        )


@router.get(
    "/",
    response_model=list[TopicResponse],
    description="Get a list of topics.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error."
        },
    },
)
async def get_topics(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        service = TopicService(TopicRepository(session))
        topics = service.get_topics()
        return topics if topics is not None else []
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {err}",
        )
