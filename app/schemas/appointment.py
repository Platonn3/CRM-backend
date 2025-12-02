from datetime import date, time

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    date: date
    start_time: time
    finish_time: time
    price: int = Field(..., ge=0)
    client_id: int
    service_id: int
    master_id: int

class AppointmentResponse(BaseModel):
    date: date
    start_time: time
    finish_time: time
    price: int

    class Config:
        from_attributes = True

class AppointmentId(BaseModel):
    date: date
    start_time: time
    finish_time: time
    master_id: int

