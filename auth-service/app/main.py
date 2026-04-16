from fastapi import FastAPI
from app.db.database import Base, engine
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Auth service is running"}