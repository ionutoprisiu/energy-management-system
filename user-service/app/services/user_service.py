from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateRequest, UserUpdateRequest

def create_user(db: Session, request: UserCreateRequest):
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        username=request.username,
        name=request.name,
        email=request.email, 
        address=request.address,
        role=request.role.value,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def update_user(db: Session, user_id: int, request: UserUpdateRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_username = db.query(User).filter(User.username == request.username, User.id != user_id).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == request.email, User.id != user_id).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    user.username = request.username
    user.name = request.name
    user.email = request.email
    user.address = request.address
    user.role = request.role.value

    db.commit()
    db.refresh(user)

    return user



def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()