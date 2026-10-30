from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.schemas import ReadingCreate, ReadingResponse
from app.models.models import Reading


def create_reading(db: Session, schema: ReadingCreate) -> ReadingResponse:

    reading_data = schema.model_dump(exclude_unset=True)
    new_reading = Reading(**reading_data)
    

    # Add the new reading to the session and commit
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    # Return the created reading as a Pydantic model
    return ReadingResponse.model_validate(new_reading)