from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from api.models import (
    TopicPreferencesItem,
    TopicPreferencesUpdatedItem,
    TopicPreferencesResponse,
    TopicCategoryItem,
    TopicItem,
)
from api.controllers.topic_preferences_controller import TopicPreferenceController
from api.controllers.topic_controller import TopicController
from api.services.topic_preferences_service import TopicPreferencesService
from api.services.topic_service import TopicService
from api.repositories.topic_preferences_repository import TopicPreferencesRepository
from api.repositories.topic_repository import TopicRepository
from storage.database import Database
from api.exceptions import (
    TopicPreferencesDuplicated,
    TopicPreferencesNotFound,
    TopicCategoryDuplicated,
)

app = FastAPI(title="Assignment TopicPreferencesService Api")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"]
)

database = Database()
topic_preferences_repository = TopicPreferencesRepository(database)
topic_preferences_service = TopicPreferencesService(topic_preferences_repository)
topic_preferences_controller = TopicPreferenceController(topic_preferences_service)

topic_category_repository = TopicRepository(database)
topic_category_service = TopicService(topic_category_repository)
topic_category_controller = TopicController(topic_category_service)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences answer of email sender\
        and students from its group if it belongs to one.",
    response_description="List of created topic preferences answers of email sender\
        and students from its group if it belongs to one.",
    response_model=List[TopicPreferencesResponse],
    responses={
        201: {"description": "Successfully added topic preferences"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    try:
        new_item = topic_preferences_controller.add_topic_preferences(topic_preferences)
        return new_item
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")


@app.put(
    "/topic_preferences/{email_sender}",
    status_code=200,
    description="Update an existing topic preferences answer of email sender and\
        students from its group if it belongs to one.",
    response_description="List of updated topic preferences answers of email sender and\
        students from its group if it belongs to one.",
    response_model=List[TopicPreferencesResponse],
    responses={
        200: {"description": "Successfully updated topic preferences"},
        409: {"description": "Student not found"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def update_topic_preferences(
    email_sender: str,
    topic_preferences_update: TopicPreferencesUpdatedItem,
):
    try:
        updated_items = topic_preferences_controller.update_topic_preferences(
            email_sender, topic_preferences_update
        )
        return updated_items
    except TopicPreferencesNotFound as err:
        raise HTTPException(
            status_code=409, detail=f"Topic preferences of '{email_sender}' not found."
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")


@app.post(
    "/topic_category/",
    status_code=201,
    description="This endpoint creates a new topic category.",
    response_description="Created topic category.",
    response_model=TopicCategoryItem,
    responses={
        201: {"description": "Successfully added topic category"},
        409: {"description": "Topic category duplicated"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def add_topic_category(topic_category: TopicCategoryItem):
    try:
        new_item = topic_category_controller.add_topic_category(topic_category)
        return new_item
    except TopicCategoryDuplicated:
        raise HTTPException(
            status_code=409,
            detail=f"Topic category '{topic_category.name}' already exists.",
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")


@app.post(
    "/topic/",
    status_code=201,
    description="This endpoint creates a new topic.",
    response_description="Created topic.",
    response_model=TopicItem,
    responses={
        201: {"description": "Successfully added topic"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def add_topic(topic: TopicItem):
    try:
        return topic
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")
