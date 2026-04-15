from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Credential
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.security import hash_password, verify_password, create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Credential).filter(Credential.username == request.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(request.password)

    new_user = Credential(
        username = request.username,
        hashed_password = hashed_password,
        role = request.role 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Credential).filter(Credential.username == request.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token({
        "username": user.username,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get("/verify")
def verify(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    parts = authorization.split(" ")
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload