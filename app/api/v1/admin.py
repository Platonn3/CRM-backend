from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from watchfiles import awatch

from app.api.v1.clients import get_master_service, get_client_service, get_appointment_service, get_service_service
from app.database.models import Master as MasterModel, Service as ServiceModel, Appointment as AppointmentModel, Client as ClientModel
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

from app.schemas.master import MasterResponse, MasterCreate, MasterWithServices

from app.database.connect import config
from app.schemas.service import ServiceResponse, ServiceCreate


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/masters",
    status_code=status.HTTP_201_CREATED,
    response_model=MasterResponse,
    summary="Создать нового мастера"
)
async def create_master(master_data: MasterCreate, service = Depends(get_master_service)):
    return await service.create_master(master_data)


@router.post(
    "/services",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceResponse,
    summary="Создать новую услугу"
)
async def create_service(service_data: ServiceCreate, service = Depends(get_service_service)):
    return await service.create_service(service_data)


@router.post(
    "/appointments",
    status_code=status.HTTP_201_CREATED,
    response_model=AppointmentResponse,
    summary="Создать новую запись"
)
async def create_appointment(appointment_data: AppointmentCreate, service = Depends(get_appointment_service)):
    return await service.create_slot(appointment_data)


@router.post(
    "/masters/{master_id}/services/{service_id}",
    status_code=status.HTTP_200_OK,
    response_model=MasterWithServices,
    summary="Добавить услугу к мастеру"
)
async def add_service_to_master(master_id: int, service_id: int, service = Depends(get_master_service)):
    return await service.add_service_to_master(master_id, service_id)


@router.delete(
    "/appointments/{appointment_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentResponse,
    summary="Удалить услугу"
)
async def delete_appointment(appointment_id: int, service = Depends(get_appointment_service)):
    return await service.delete_appointment(appointment_id)