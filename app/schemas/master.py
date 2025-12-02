from typing import List

from pydantic import BaseModel, Field
from app.schemas.service import ServiceResponse
from app.schemas.appointment import AppointmentResponse


class MasterCreate(BaseModel):
    name: str = Field(..., max_length=30)
    surname: str = Field(..., max_length=80)
    phone: str = Field(..., min_length=10, max_length=20)

class MasterResponse(BaseModel):
    id: int
    name: str
    surname: str
    phone: str

    class Config:
        from_attributes = True

class MasterWithServices(MasterResponse):
    services: List[ServiceResponse] = []

class MasterWithAppointments(MasterResponse):
    appointments: List[AppointmentResponse] = []

class MasterId(BaseModel):
    master_phone: str