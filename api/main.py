from fastapi import FastAPI

app = FastAPI()


@app.get(
    "/", summary="Root Endpoint", description="This endpoint returns a ping message."
)
async def root():
    return "Ping"
