from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


@app.get(
    "/", summary="Root Endpoint", description="This endpoint returns a ping message."
)
async def root():
    return "Ping"


class TopicPreferencesItem(BaseModel):
    email: str
    group_id: datetime
    topic1: str
    topic2: str
    topic3: str


@app.post("/topic_preferences/", status_code=201)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    return topic_preferences
