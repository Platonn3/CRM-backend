from typing import Optional

from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    surname: Optional[str] = Field(None, max_length=80)
    phone: str = Field(..., min_length=10, max_length=20, pattern=r"^\d+$")
    tg_id: Optional[str] = Field(None, max_length=50)

class ClientResponse(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    phone: str
    tg_id: Optional[str]

    class Config:
        from_attributes = True