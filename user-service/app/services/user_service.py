from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateRequest, UserUpdateRequest

def create_user(db: Session, request: UserCreateRequest):
    pass

def get_all_users(db: Session):
    pass

def get_user_by_id(db: Session, user_id: int):
    pass

def update_user(db: Session, user_id: int, request: UserUpdateRequest):
    pass

def delete_user(db: Session, user_id: int):
    pass