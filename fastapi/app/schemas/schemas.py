from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Used when creating a new reading
class ReadingCreate(BaseModel):
    sensor: str = Field(min_length=1, max_length=50)
    content: float = Field(ge=0, le=100)
    user_id: int = Field(gt=0)


# Used when updating an existing reading
class ReadingUpdate(BaseModel):
    sensor: str | None = Field(default=None, min_length=1, max_length=50)
    content: float | None = Field(default=None, ge=0, le=100)


# Used when returning a reading to the client
class ReadingResponse(BaseModel):
    id: int
    sensor: str
    content: float
    user_id: int
    date_timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
