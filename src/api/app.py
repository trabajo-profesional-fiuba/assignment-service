from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.api.auth.router import router as auth_router
from src.api.forms.router import router as form_router
from src.api.groups.router import router as group_router
from src.api.students.router import router as student_router
from src.api.topics.router import router as topic_router
from src.api.tutors.router import router as tutor_router
from src.api.assignments.router import router as assignment_router

from src.config.config import api_config
from src.config.database.database import create_tables
from src.config.logging import logger


api_description = """

## Group 54 - Final Project

The Assignment Management API is designed to optimize the allocation of resources and
scheduling within educational projects. Key functionalities include:

- **Group Assignments**: Allocate individuals to incomplete student groups.
- **Topic and Tutor Assignments**: Assign relevant topics and tutors to student
groups.
- **Presentation Scheduling**: Set and manage presentation dates for each group.

This API is crucial for efficiently matching group members, topics, and presentation
slots, ensuring effective project organization and execution.

**Key Entities**:
- Students
- Groups
- Tutors
- Topics
- Categories

Interact with these entities through a series of dedicated API endpoints tailored to
facilitate smooth and effective assignments.

## Contributors
- Celeste Dituro       - cdituro@fi.uba.ar
- Victoria Abril Lopez - vlopez@fi.uba.ar
- Iván Lautaro Pfaab   - ipfaab@fi.uba.ar
- Alejo Villores       - avillores@fi.uba.ar
"""
logger.info("Initializing databases")
create_tables()

logger.info("Instanciating FastAPI App")
app = FastAPI(
    title="Assignment Service Api",
    version=api_config.api_version,
    description=api_description,
    redoc_url=None,
    docs_url="/docs",
    root_path="/api",
)
logger.info("Adding authentication router")
app.include_router(auth_router)
logger.info("Adding student router")
app.include_router(student_router)
logger.info("Adding tutors router")
app.include_router(tutor_router)
logger.info("Adding topics router")
app.include_router(topic_router)
logger.info("Adding forms router")
app.include_router(form_router)
logger.info("Adding groups router")
app.include_router(group_router)
logger.info("Adding assigments router")
app.include_router(assignment_router)
logger.info("Adding middlewares")
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
