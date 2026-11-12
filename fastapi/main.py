# uv run uvicorn main:app --reload
from fastapi import FastAPI
from readings import router as readings_router

app = FastAPI()

app.include_router(readings_router)