# uv run uvicorn app.main:app --reload
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import Base, engine, get_db
from app.models import models

# Get paths relative to this file
APP_DIR = Path(__file__).resolve().parent

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soil Moisture Monitor")

# Static files
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")

# HTML templates
templates = Jinja2Templates(directory=APP_DIR / "templates")


@app.get("/", include_in_schema=False, name="home")
@app.get("/sensor_readings", include_in_schema=False, name="sensor_readings")
def sensor_readings(request: Request,db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Reading))                     
    readings = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "sensor_readings": readings,
            "title": "Sensor Readings"
        }
    )