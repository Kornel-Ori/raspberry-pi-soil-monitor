from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

#--------Users
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


#--------Plant_Species
class PlantSpeciesBase(BaseModel):
    common_name: str = Field(min_length=1, max_length=100)
    botanical_name: str | None = None
    description: str | None = None
    min_moisture: float = Field(ge=0, le=100)

class PlantSpeciesCreate(PlantSpeciesBase):
    pass


class PlantSpeciesResponse(PlantSpeciesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


#--------Plant
class PlantBase(BaseModel):
    plant_name: str = Field(min_length=1, max_length=100)
    location: str | None = None
    min_moisture: float | None = Field(default=None, ge=0, le=100)
    image_url: str | None = Field(default=None, max_length=255)


class PlantCreate(PlantBase):
    user_id: int
    species_id: int


class PlantResponse(PlantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    species_id: int
    created_at: datetime

class PlantUpdate(BaseModel):
    plant_name: str | None = Field(default=None, min_length=1, max_length=100)
    location: str | None = Field(default=None)
    min_moisture: float | None = Field(default=None, ge=0, le=100)

#--------Node
class NodeBase(BaseModel):
    device_name: str = Field(min_length=1, max_length=100)
    status: str = "offline"
    led_status: str = "off"


class NodeCreate(NodeBase):
    plant_id: int


class NodeResponse(NodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plant_id: int | None
    last_seen: datetime | None
    created_at: datetime

#--------Readings
class ReadingBase(BaseModel):
    moisture_percent: float = Field(ge=0, le=100)


class ReadingCreate(ReadingBase):
    node_id: int


class ReadingUpdate(BaseModel):
    moisture_percent: float | None = Field(default=None, ge=0, le=100)


class ReadingResponse(ReadingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id: int
    recorded_at: datetime


#--------Alerts
class AlertBase(BaseModel):
    message: str
    status: str = "active"


class AlertCreate(AlertBase):
    plant_id: int
    reading_id: int | None = None


class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plant_id: int
    reading_id: int | None
    created_at: datetime
    resolved_at: datetime | None
