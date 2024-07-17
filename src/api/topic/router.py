from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session


from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicReponse
)
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
import src.api.topic.exceptions as exceptions

from src.config.database import get_db


router = APIRouter(prefix="/topics", tags=["topics"])


@router.post(
    "/category",
    status_code=status.HTTP_201_CREATED,
    description="This endpoint creates a new category for a topic.",
    response_description="Created topic category.",
    response_model=CategoryResponse,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added topic category"},
        status.HTTP_409_CONFLICT: {"description": "Topic category duplicated"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)
async def add_category(category: CategoryRequest, session: Annotated[Session, Depends(get_db)]):
    try:
        service = TopicService(TopicRepository(session))
        category_added = service.add_category(category)
        return category_added
    except exceptions.CategoryDuplicated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Topic category '{category.name}' already exists.",
        )
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error {err}")
    

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="This endpoint creates a new topic.",
    response_description="Created topic.",
    response_model=TopicReponse,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added topic"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)
async def add_topic(topic: TopicRequest, session: Annotated[Session, Depends(get_db)]):
    try:
        service = TopicService(TopicRepository(session))
        topic_added = service.add_topic(topic)
        return topic_added
    except (exceptions.InsertTopicException, exceptions.TopicCategoryNotFound) as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error.message,
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")