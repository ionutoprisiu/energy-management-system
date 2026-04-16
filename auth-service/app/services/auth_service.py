from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.credential import Credential
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, username: str, password: str, role: str):
    existing_user = db.query(Credential).filter(Credential.username == username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(password)

    new_user = Credential(
        username=username,
        hashed_password=hashed_password,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, username: str, password: str):
    user = db.query(Credential).filter(Credential.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }