from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.schemas import ReadingCreate, ReadingResponse
from app.models.models import Reading


def create_reading(db: Session, schema: ReadingCreate) -> ReadingResponse:

    reading_data = schema.model_dump(exclude_unset=True) #so that fields the client didn't provide remain unchanged.
    new_reading = Reading(**reading_data)
    

    # Add the new reading to the session and commit
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    # Return the created reading as a Pydantic model
    return ReadingResponse.model_validate(new_reading)


def get_readings(db: Session) -> list[ReadingResponse]:
    result = db.execute(select(Reading))
    readings = result.scalars().all()

    # Convert the list of Reading objects to a list of ReadingResponse objects
    return [ReadingResponse.model_validate(reading) for reading in readings]


def get_reading_by_id(db: Session, reading_id: int) -> ReadingResponse | None:
    reading = db.get(Reading, reading_id) #SELECT * FROM reading WHERE id = ?;
    if reading is None:
        return None

    return ReadingResponse.model_validate(reading)


def update_reading(db: Session, reading_id: int, schema: ReadingCreate) -> ReadingResponse | None:
    reading = db.get(Reading, reading_id)
    if reading is None:
        return None

    # Update the reading with the new data
    updated_data = schema.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(reading, key, value)

    db.commit()
    db.refresh(reading)

    return ReadingResponse.model_validate(reading)


def delete_reading(db: Session, reading_id: int) -> bool:
    reading = db.get(Reading, reading_id)
    if reading is None:
        return False

    db.delete(reading)
    db.commit()
    return True