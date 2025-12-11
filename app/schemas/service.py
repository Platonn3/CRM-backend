from datetime import time

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    id: int
    name: str = Field(..., max_length=255)
    duration: time
    description: str | None = None
    default_price: int = Field(..., ge=0)

class ServiceResponse(BaseModel):
    name: str = Field(..., max_length=255)
    duration: time
    description: str
    default_price: int

    class Config:
        from_attributes = True

class ServiceId(BaseModel):
    name: str
    description: str
    default_price: int