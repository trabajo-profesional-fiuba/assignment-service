from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.api.assignments.router import router as assignment_router
from src.api.auth.router import router as auth_router
from src.api.dates.router import router as dates_router
from src.api.forms.router import router as form_router
from src.api.groups.router import router as group_router
from src.api.periods.router import router as period_router
from src.api.students.router import router as student_router
from src.api.topics.router import router as topic_router
from src.api.tutors.router import router as tutor_router
from src.api.periods.router import router as period_router
from src.api.assignments.router import router as assignment_router
from src.api.dates.router import router as dates_router
from src.api.admins.router import router as admins_router

from src.config.config import api_config
from src.config.database.database import init_default_values
from src.config.logging import logger


api_description = """

## Group 54 - Trabajo Profesional

The Assignment Management API fue diseñado para optimizar las diferentes asignaciones que se producen 
durante el cuatrimestre de la cursada.

Ademas, a través de sus diferentes endpoints se puede crear cuatrimestres, crear grupos, realizar seguimiento,
enviar notificaciones por mail y mucho mas

Posee tres asignaciones principales

1. Asignacion de estudiantes a grupos incompletos
2. Asignacion de grupos a temas y tutores
3. Asignacion de grupos a fechas de exposicion.

Para realizar estas asignaciones, se utilizan algoritmos de programacion lineal y redes de flujo.

## Desarrolladores
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
    ("admins", admins_router),
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
