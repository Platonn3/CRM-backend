from datetime import date, time

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    date: date
    start_time: time
    finish_time: time
    price: int = Field(..., ge=0)
    client_id: int = 0
    service_id: int
    master_id: int

class AppointmentResponse(BaseModel):
    id: int
    date: date
    start_time: time
    finish_time: time
    price: int
    client_id: int
    master_id: int

    class Config:
        from_attributes = True

class AppointmentId(BaseModel):
    date: date
    start_time: time
    finish_time: time
    master_id: int

