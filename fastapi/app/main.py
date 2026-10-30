# uv run uvicorn app.main:app --reload
from fastapi import FastAPI
from app.routers.readings import router as readings_router

app = FastAPI()

app.include_router(readings_router)