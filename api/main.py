from fastapi import FastAPI, Depends, HTTPException
from api.repository import Repository
from api.service import TopicTutorService
from api.models import TopicPreferencesItem
from api.database import Database

app = FastAPI()
database = Database()
session = database.setup()
repository = Repository(session)
service = TopicTutorService(repository)


@app.get(
    "/", summary="Root Endpoint", description="This endpoint returns a ping message."
)
async def root():
    return "Ping"


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences.",
)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    response = service.add_topic_preferences(topic_preferences)
    return response
