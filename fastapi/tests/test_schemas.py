from app.schemas.schemas import ReadingCreate

reading = ReadingCreate(
    sensor="Plant Sensor 1",
    content=35.5,
    user_id=1
)

print(reading)
print(reading.model_dump())