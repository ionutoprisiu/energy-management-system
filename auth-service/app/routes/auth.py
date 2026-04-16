from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, MessageResponse
from app.dependencies.auth import get_current_user
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=MessageResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    register_user(
        db=db,
        username=request.username,
        password=request.password,
        role=request.role.value
    )

    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        username=request.username,
        password=request.password
    )


@router.get("/verify")
def verify(current_user=Depends(get_current_user)):
    return current_user


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return current_user