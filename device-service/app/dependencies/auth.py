from fastapi import Header, HTTPException

from app.core.security import verify_token

def get_current_user(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    parts = authorization.split()

    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload

def require_admin(authorization: str = Header(..., alias="Authorization")):
    user = get_current_user(authorization)

    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user