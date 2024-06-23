from fastapi import FastAPI, HTTPException
from api.repository import Repository
from api.service import Service
from api.models import TopicPreferencesItem
from api.database import Database
from api.exceptions import TopicPreferencesDuplicated

app = FastAPI()
database = Database()
session = database.setup()
repository = Repository(session)
service = Service(repository)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences.",
)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    try:
        response = service.add_topic_preferences(topic_preferences)
        return response
    except TopicPreferencesDuplicated as e:
        raise HTTPException(status_code=409, detail="Topic preference already exists.")


@app.patch(
    "/topic_preferences/{email}",
    status_code=200,
    description="Update an existing topic preferences.",
)
async def update_topic_preferences(
    topic_preferences_update: TopicPreferencesItem,
):
    email = topic_preferences_update.email
    updated_preferences = service.update_topic_preferences(
        email, topic_preferences_update
    )
    return topic_preferences_update
