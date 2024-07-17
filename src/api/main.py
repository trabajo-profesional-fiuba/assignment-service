import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import create_tables
from src.api.student.router import router as student_router
from src.api.topic.router import router as topic_router
from src.api.form.router import router as form_router


create_tables()

app = FastAPI(title="Assignment Service Api")
app.include_router(student_router)
app.include_router(topic_router)
app.include_router(form_router)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"]
)

@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)