from pydantic import BaseModel


class DeviceCreateRequest(BaseModel):
    name: str
    max_consumption: float


class DeviceUpdateRequest(BaseModel):
    name: str
    max_consumption: float


class DeviceResponse(BaseModel):
    id: int
    name: str
    max_consumption: float
    user_id: int | None = None

    class Config:
        from_attributes = True


class AssignDeviceRequest(BaseModel):
    user_id: int


class MessageResponse(BaseModel):
    message: str
