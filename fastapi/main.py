# uv run uvicorn main:app --reload
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
#from mqtt_listener import start_mqtt_listener, stop_mqtt_listener
from schemas import ReadingCreate, ReadingResponse, ReadingUpdate


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/readings/", response_model=list[ReadingResponse])
def get_all_readings(db: Session = Depends(get_db)):
    result = db.execute(select(models.Reading))
    return result.scalars().all()

@app.get("/readings/{reading_id}", response_model=ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return result


@app.post("/readings/", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
def create_new_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    result = models.Reading(**reading.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@app.put("/readings/{reading_id}", response_model=ReadingResponse)
def update_existing_reading(reading_id: int, reading: ReadingUpdate, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    for key, value in reading.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result


@app.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_reading(reading_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    db.delete(result)
    db.commit()
    return None