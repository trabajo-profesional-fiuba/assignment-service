import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.topic_preferences_repository import TopicPreferencesRepository
from api.topic_preferences_service import TopicPreferencesService
from api.models import (
    TopicPreferencesItem,
    TopicPreferencesUpdatedItem,
    TopicPreferencesResponse,
)
from storage.database import Database
from api.exceptions import TopicPreferencesDuplicated, StudentNotFound
from api.topic_preferences_controller import TopicPreferenceController
from typing import List
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Assignment TopicPreferencesService Api")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"]
)

database = Database(DATABASE_URL)
repository = TopicPreferencesRepository(database)
service = TopicPreferencesService(repository)
controller = TopicPreferenceController(service)


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
        409: {"description": "Topic preferences duplicated"},
        422: {"description": "Validation Error"},
    },
)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    try:
        new_item = controller.add_topic_preferences(topic_preferences)
        return new_item
    except TopicPreferencesDuplicated:
        raise HTTPException(status_code=409, detail="Topic preference already exists.")


@app.put(
    "/topic_preferences/{email}",
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
    },
)
async def update_topic_preferences(
    email: str,
    topic_preferences_update: TopicPreferencesUpdatedItem,
):
    try:
        updated_items = controller.update_topic_preferences(
            email, topic_preferences_update
        )
        return updated_items
    except StudentNotFound as err:
        raise HTTPException(status_code=409, detail=f"Student '{err}' not found.")
