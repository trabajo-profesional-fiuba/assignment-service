from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from src.config.database.database import create_tables

from src.api.student.router import router as student_router
from src.api.topic.router import router as topic_router
from src.api.form.router import router as form_router
from src.api.tutors.router import router as tutor_router
from src.api.auth.router import router as auth_router
from src.api.groups.router import router as group_router


create_tables()

app = FastAPI(title="Assignment Service Api", version="1.0.0")
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(topic_router)
app.include_router(form_router)
app.include_router(tutor_router)
app.include_router(group_router)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"]
)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return RedirectResponse("/docs")
