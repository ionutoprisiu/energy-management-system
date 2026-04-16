from enum import Enum 

from pydantic import BaseModel

class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: RoleEnum

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum

class MessageResponse(BaseModel):
    message: str