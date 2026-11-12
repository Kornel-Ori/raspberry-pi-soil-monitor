# uv run uvicorn main:app --reload
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from auth import hash_password
#from mqtt_listener import start_mqtt_listener, stop_mqtt_listener
from schemas import NodeCreate, NodeResponse, PlantCreate, PlantResponse, PlantSpeciesResponse, PlantUpdate, ReadingCreate, ReadingResponse, ReadingUpdate, UserResponse, UserCreate, UserUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False, name="home")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"title": "Plant Soil Level"})


#--------Users
@app.get("/users/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    result = db.execute(select(models.User))
    return result.scalars().all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = db.get(models.User, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    result = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password))
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@app.patch("/users/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    result = db.get(models.User, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result   


#--------PlantsSpecies
@app.get("/plants_species/", response_model=list[PlantSpeciesResponse])
def get_all_plants_species(db: Session = Depends(get_db)):
    result = db.execute(select(models.PlantSpecies))
    return result.scalars().all()

@app.get("/plants_species/{species_id}", response_model=PlantSpeciesResponse)
def get_plant_species(species_id: int, db: Session = Depends(get_db)):
    result = db.get(models.PlantSpecies, species_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant species not found")
    return result


#--------Plants
@app.get("/plants/", response_model=list[PlantResponse])
def get_all_plants(db: Session = Depends(get_db)):
    result = db.execute(select(models.Plant))
    return result.scalars().all()

@app.get("/plants/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return result

@app.post("/plants/", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_new_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    result = models.Plant(**plant.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

@app.patch("/plants/{plant_id}", response_model=PlantResponse)
def update_existing_plant(plant_id: int, plant: PlantUpdate, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    for key, value in plant.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result   

@app.delete("/plants/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_plant(plant_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    db.delete(result)
    db.commit()
    return None


#--------Nodes
@app.get("/nodes/", response_model=list[NodeResponse])
def get_all_nodes(db: Session = Depends(get_db)):
    result = db.execute(select(models.Node))
    return result.scalars().all()


@app.get("/nodes/{node_id}", response_model=NodeResponse)
def get_node(node_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return result


@app.patch("/nodes/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
def create_new_node(node: NodeCreate, db: Session = Depends(get_db)):
    result = models.Node(**node.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@app.patch("/nodes/{node_id}", response_model=NodeResponse)
def update_existing_node(node_id: int, node: NodeCreate, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    for key, value in node.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result   


@app.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_node(node_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    db.delete(result)
    db.commit()
    return None

#--------Readings
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


@app.patch("/readings/{reading_id}", response_model=ReadingResponse)
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