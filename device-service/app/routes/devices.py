from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.schemas.device import (
    AssignDeviceRequest,
    DeviceCreateRequest,
    DeviceResponse,
    DeviceUpdateRequest,
    MessageResponse,
)
from app.services.device_service import (
    assign_device,
    create_device,
    delete_device,
    get_all_devices,
    get_device_by_id,
    get_my_devices,
    unassign_device,
    update_device,
)

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("", response_model=DeviceResponse)
def create_device_route(
    request: DeviceCreateRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return create_device(db=db, request=request)


@router.get("", response_model=list[DeviceResponse])
def list_devices_route(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return get_all_devices(db=db)


@router.get("/me", response_model=list[DeviceResponse])
def my_devices_route(
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    if current.get("role") != "client":
        raise HTTPException(status_code=403, detail="Client access required")
    uid = current.get("user_id")
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return get_my_devices(db=db, user_id=int(uid))


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device_route(
    device_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return get_device_by_id(db=db, device_id=device_id)


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device_route(
    device_id: int,
    request: DeviceUpdateRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return update_device(db=db, device_id=device_id, request=request)


@router.delete("/{device_id}", response_model=MessageResponse)
def delete_device_route(
    device_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    delete_device(db=db, device_id=device_id)
    return {"message": "Device deleted successfully"}


@router.post("/{device_id}/assign", response_model=DeviceResponse)
def assign_device_route(
    device_id: int,
    request: AssignDeviceRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return assign_device(db=db, device_id=device_id, user_id=request.user_id)


@router.post("/{device_id}/unassign", response_model=DeviceResponse)
def unassign_device_route(
    device_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return unassign_device(db=db, device_id=device_id)
