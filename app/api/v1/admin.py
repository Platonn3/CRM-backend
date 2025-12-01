from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Master as MasterModel, Service as ServiceModel, Appointment as AppointmentModel, Client as ClientModel
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

from app.schemas.master import MasterResponse, MasterCreate, MasterWithServices

from app.database.connect import config
from app.schemas.service import ServiceResponse, ServiceCreate


router = APIRouter(prefix="/admin", tags=["admin"])

