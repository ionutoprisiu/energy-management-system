from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import require_admin
from app.schemas.user import UserCreateRequest, UserUpdateRequest, UserResponse, MessageResponse
from app.services.user_service import create_user, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse)
def create_user_route(request: UserCreateRequest, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return create_user(db=db, request=request)

@router.get("", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return get_all_users(db=db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return get_user_by_id(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, request: UserUpdateRequest, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return update_user(db=db, user_id=user_id, request=request)

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user_route(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}