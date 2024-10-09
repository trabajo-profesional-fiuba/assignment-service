from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.api.auth.router import router as auth_router
from src.api.forms.router import router as form_router
from src.api.groups.router import router as group_router
from src.api.students.router import router as student_router
from src.api.topics.router import router as topic_router
from src.api.tutors.router import router as tutor_router
from src.api.periods.router import router as period_router
from src.api.assignments.router import router as assignment_router
from src.api.dates.router import router as dates_router

from src.config.config import api_config
from src.config.database.database import init_default_values
from src.config.logging import logger


api_description = """

## Group 54 - Final Project

The Assignment Management API is designed to optimize the allocation of resources and
scheduling within educational projects. Key functionalities include:

The API, Assignment Management is design to optimize the allocation of resources and
scheduling within educational projects. Key functionalities include:

- Group Assignments: Divide individuals to incomplete student groups.

- Topic and Tutor Assignments: Assign relevant topics and tutors to student
groups.

- Presentation Scheduling: Set and manage presentation dates for each group.

This API is crucial for matching group members, topics, and presentation
slots, ensuring effective project organization and execution.

**Key Entities**:
- Students
- Groups
- Tutors
- Topics
- Categories
- Period

Interact with these entities through a series of dedicated API endpoints tailored to
facilitate smooth and effective assignments.

## Contributors
- Celeste Dituro       - cdituro@fi.uba.ar
- Victoria Abril Lopez - vlopez@fi.uba.ar
- Iván Lautaro Pfaab   - ipfaab@fi.uba.ar
- Alejo Villores       - avillores@fi.uba.ar
"""
logger.info("Initializing all the database default values.")
init_default_values()

# List of routers to add
routers = [
    ("authentication", auth_router),
    ("period", period_router),
    ("student", student_router),
    ("tutors", tutor_router),
    ("topics", topic_router),
    ("forms", form_router),
    ("groups", group_router),
    ("assignments", assignment_router),
    ("dates", dates_router),
]


logger.info("Instanciating FastAPI App")
app = FastAPI(
    title="Assignment Service Api",
    version=api_config.api_version,
    description=api_description,
    redoc_url=None,
    docs_url="/docs",
    root_path="/api",
)
# Adding routers
for name, router in routers:
    logger.info(f"Adding {name} router")
    app.include_router(router)


logger.info("Adding api middlewares")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/", description="This endpoint redirects to docs")
async def root(request: Request):
    docs_url = str(request.base_url) + "docs"
    return RedirectResponse(docs_url)


@app.get("/version", description="Returns the current version of the api")
async def version():
    return api_config.api_version
