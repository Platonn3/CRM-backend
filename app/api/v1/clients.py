from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from app.database.connect import config
from app.repositories.appointment import AppointmentRepository
from app.repositories.client import ClientRepository
from app.repositories.master import MasterRepository
from app.repositories.service import ServiceRepository
from app.schemas.client import ClientCreate, ClientResponse
from app.schemas.master import MasterResponse, MasterWithServices, MasterWithAppointments
from app.schemas.service import ServiceResponse
from app.schemas.appointment import AppointmentResponse
from app.database.models import Client as ClientModel
from app.database.models import Master as MasterModel
from app.database.models import Service as ServiceModel
from app.database.models import Appointment as AppointmentModel
from app.services.appointment import AppointmentService
from app.services.client import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_service(db: AsyncSession = Depends(config.get_db)):
    repo = ClientRepository(ClientModel, db)
    return ClientService(repo)


def get_appointment_service(db: AsyncSession = Depends(config.get_db)):
    appt_repo = AppointmentRepository(AppointmentModel, db)
    client_repo = ClientRepository(ClientModel, db)
    service_repo = ServiceRepository(ServiceModel, db)
    master_repo = MasterRepository(MasterModel, db)
    return AppointmentService(client_repo, master_repo, service_repo, appt_repo)


@router.post(
    path="/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового клиента"
)
async def create_new_client(client_data: ClientCreate, service = Depends(get_client_service)):
    return await service.create_client(client_data)


@router.get(
    "/",
    response_model=list[ClientResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить всех клиентов"
)
async def get_all_clients(service = Depends(get_client_service)):
    return await service.get_all_clients()


@router.get(
    "/by_tg_id/{tg_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить клиента по tg ID"
)
async def get_client_by_tg_id(tg_id: str, service = Depends(get_client_service)):
    return await service.get_client_by_tg_id(tg_id)


@router.post(
    "/{client_id}/appointments/{appointment_id}",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Записать клиента на услугу"
)
async def sign_up_client_on_appointment(client_id: int, appointment_id: int, service = Depends(get_appointment_service)):
    return await service.book_slot(client_id, appointment_id)
