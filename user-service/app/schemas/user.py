from enum import Enum

from pydantic import BaseModel

class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"

class UserCreateRequest(BaseModel):
    username: str
    name: str
    email: str
    address: str | None = None
    role: RoleEnum

class UserUpdateRequest(BaseModel):
    username: str
    name: str
    email: str
    address: str | None = None
    role: RoleEnum

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    address: str | None = None
    role: RoleEnum

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str