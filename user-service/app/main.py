from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "User service is running"}