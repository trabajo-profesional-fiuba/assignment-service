from fastapi import FastAPI, HTTPException
from api.repository import Repository
from api.service import Service
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem, TopicPreferencesResponse
from api.database import Database
from api.exceptions import TopicPreferencesDuplicated, StudentNotFound
from api.controller import Controller

app = FastAPI(title="Assignment Service Api")
database = Database()
session = database.setup()
repository = Repository(session)
service = Service(repository)
controller = Controller(service)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences answer of email sender and students from its group if it belongs to one.",
    response_description="List of created topic preferences answers of email sender and students from its group if it belongs to one.",
    response_model=TopicPreferencesResponse,
    responses={
        201: {"description": "Successfully added topic preferences"},
        409: {"description": "Topic preferences duplicated"},
        422: {"description": "Validation Error"},
    }
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
    description="Update an existing topic preferences answer of email sender and students from its group if it belongs to one.",
    response_description="List of updated topic preferences answers of email sender and students from its group if it belongs to one.",
    response_model=TopicPreferencesResponse,
    responses={
        200: {"description": "Successfully updated topic preferences"},
        409: {"description": "Student not found"},
        422: {"description": "Validation Error"},
    }
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
    except StudentNotFound:
        raise HTTPException(status_code=409, detail="Student not found.")
