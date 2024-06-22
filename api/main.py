from fastapi import FastAPI, Depends, HTTPException
from api.repository import Repository
from api.models import TopicPreferencesItem

app = FastAPI()
repository = Repository()


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
    response = repository.add_topic_preferences(topic_preferences)
    return response
