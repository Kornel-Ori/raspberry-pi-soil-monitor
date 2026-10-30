from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.schemas import ReadingCreate, ReadingUpdate, ReadingResponse

from app.services.reading_service import (
    create_reading,
    get_readings,
    get_reading_by_id,
    update_reading,
    delete_reading
)


router = APIRouter(prefix="/readings", tags=["Readings"])

@router.get("/", response_model=list[ReadingResponse])
def get_all_readings(db: Session = Depends(get_db)):
    readings = get_readings(db)
    return readings

@router.get("/{reading_id}", response_model=ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = get_reading_by_id(db, reading_id)
    if reading is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return reading


@router.post("/", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
def create_new_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    new_reading = create_reading(db, reading)
    return new_reading


@router.put("/{reading_id}", response_model=ReadingResponse)
def update_existing_reading(reading_id: int, reading: ReadingUpdate, db: Session = Depends(get_db)):
    updated_reading = update_reading(db, reading_id, reading)
    if updated_reading is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return updated_reading


@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_reading(reading_id: int, db: Session = Depends(get_db)):
    success = delete_reading(db, reading_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return None

