from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.api.topic.schemas import (
    TopicPreferencesItem,
    TopicPreferencesResponse,
    TopicCategoryItem,
    TopicItem,
)
from src.api.topic.router import TopicController
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.config.database import Database
from src.api.topic.exceptions import (
    TopicCategoryDuplicated,
    TopicCategoryNotFound,
    TopicDuplicated,
    StudentEmailDuplicated,
)

app = FastAPI(title="Assignment Service Api")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"]
)

database = Database()
topic_repository = TopicRepository(database)
topic_service = TopicService(topic_repository)
topic_controller = TopicController(topic_service)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


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
        new_item = topic_controller.add_topic_category(topic_category)
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
        return topic_controller.add_topic(topic)
    except TopicCategoryNotFound:
        raise HTTPException(
            status_code=409,
            detail=f"Topic category '{topic.category}' not found.",
        )
    except TopicDuplicated:
        raise HTTPException(
            status_code=409,
            detail=f"Topic '{topic.name}, {topic.category}' already exists.",
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")


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
        return topic_controller.add_topic_preferences(topic_preferences)
    except StudentEmailDuplicated as email:
        raise HTTPException(
            status_code=409,
            detail=f"Student email '{email}' already exists.",
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {err}")
