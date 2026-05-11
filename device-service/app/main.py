from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes.devices import router as devices_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Device Service")

app.include_router(devices_router)


@app.get("/")
def root():
    return {"message": "Device service is running"}
