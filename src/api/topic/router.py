from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session


from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicReponse,
    TopicPreferencesRequest,
)
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
import src.api.topic.exceptions as exceptions

from src.config.database import get_db


router = APIRouter(prefix="/topics")


@router.post(
    "/categories",
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
    except exceptions.TopicCategoryDuplicated:
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
        topic_added = service.add_topic(category)
        return topic_added.add_topic(topic)
    except (exceptions.InsertTopicException, exceptions.TopicCategoryNotFound) as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")

class TopicController:

    def __init__(self, service: TopicService):
        self._service = service

    def _format_topic_category(self, item):
        return {"name": item.name}

    def add_topic_category(self, topic_category: TopicCategoryRequest):
        try:
            new_item = self._service.add_topic_category(topic_category)
            return self._format_topic_category(new_item)
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        try:
            return self._service.add_topic(topic)
        except Exception as err:
            raise err

    def _format_topic_preferences(
        self, new_items: list, request: TopicPreferencesRequest
    ):
        """
        Deletes other students from the same group email.
        """
        formatted_list = []
        for new_item in new_items:
            formatted_item = {
                "uid": new_item.uid,
                "group_id": new_item.group_id,
                "topic_1": request.topic_1,
                "category_1": request.category_1,
                "topic_2": request.topic_2,
                "category_2": request.category_2,
                "topic_3": request.topic_3,
                "category_3": request.category_3,
            }
            formatted_list.append(formatted_item)
        return formatted_list

    def add_topic_preferences(self, topic_preferences: TopicPreferencesRequest):
        try:
            new_items = self._service.add_topic_preferences(topic_preferences)
            return self._format_topic_preferences(new_items, topic_preferences)
        except Exception as err:
            raise err
