from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreateRequest, DeviceUpdateRequest


def create_device(db: Session, request: DeviceCreateRequest):
    existing = db.query(Device).filter(Device.name == request.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Device name already exists")

    device = Device(
        name=request.name,
        max_consumption=request.max_consumption,
        user_id=None,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_all_devices(db: Session):
    return db.query(Device).all()


def get_my_devices(db: Session, user_id: int):
    return db.query(Device).filter(Device.user_id == user_id).all()


def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def update_device(db: Session, device_id: int, request: DeviceUpdateRequest):
    device = get_device_by_id(db, device_id)

    conflict = (
        db.query(Device)
        .filter(Device.name == request.name, Device.id != device_id)
        .first()
    )
    if conflict:
        raise HTTPException(status_code=409, detail="Device name already exists")

    device.name = request.name
    device.max_consumption = request.max_consumption
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()


def assign_device(db: Session, device_id: int, user_id: int):
    device = get_device_by_id(db, device_id)
    device.user_id = user_id
    db.commit()
    db.refresh(device)
    return device


def unassign_device(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    device.user_id = None
    db.commit()
    db.refresh(device)
    return device
