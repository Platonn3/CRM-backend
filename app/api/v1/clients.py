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
from app.schemas.master import MasterResponse, MasterWithServices, MasterWithAppointments, MasterId
from app.schemas.service import ServiceResponse, ServiceId
from app.schemas.appointment import AppointmentResponse, AppointmentId
from app.database.models import Client as ClientModel
from app.database.models import Master as MasterModel
from app.database.models import Service as ServiceModel
from app.database.models import Appointment as AppointmentModel
from app.services.appointment import AppointmentService
from app.services.client import ClientService
from app.services.master import MasterService
from app.services.service import ServiceService

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_service(db: AsyncSession = Depends(config.get_db)):
    repo = ClientRepository(ClientModel, db)
    return ClientService(repo)


def get_master_service(db: AsyncSession = Depends(config.get_db)):
    service_repo = ServiceRepository(ServiceModel, db)
    master_repo = MasterRepository(MasterModel, db)
    return MasterService(master_repo, service_repo)


def get_service_service(db: AsyncSession = Depends(config.get_db)):
    service_repo = ServiceRepository(ServiceModel, db)
    return ServiceService(service_repo)


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


@router.get(
    "/services",
    response_model=list[ServiceResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все услуги"
)
async def get_all_services(service = Depends(get_service_service)):
    return await service.get_all_services()


@router.post(
    "/{client_id}/appointments/{appointment_id}",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Записать клиента на услугу"
)
async def sign_up_client_on_appointment(client_id: int, appointment_id: int, service = Depends(get_appointment_service)):
    return await service.book_slot(client_id, appointment_id)


@router.get(
    "/masters",
    response_model=list[MasterResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить всех мастеров"
)
async def get_all_masters(service = Depends(get_master_service)):
    return await service.get_all_masters()


@router.get(
    "/masters/{id}",
    response_model=MasterResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить мастера по ID"
)
async def get_master_by_id(master_id: int, service = Depends(get_master_service)):
    return await service.get_master_by_id(master_id)


@router.get(
    "/masters/{id}/services",
    response_model=MasterWithServices,
    status_code=status.HTTP_200_OK,
    summary="Получить все сервисы мастера"
)
async def get_master_with_services(master_id: int, service = Depends(get_master_service)):
    return await service.get_master_with_services(master_id)


@router.get(
    "/masters/{id}/appointments",
    response_model=MasterWithAppointments,
    status_code=status.HTTP_200_OK,
    summary="Получить все записи мастера"
)
async def get_master_with_appointments(master_id: int, service = Depends(get_master_service)):
    return await service.get_master_with_appointments(master_id)


@router.post(
    "/appointment_id",
    status_code=status.HTTP_200_OK,
    summary="Получить ID по данным записи"
)
async def get_id_by_appointment_data(appointment_data: AppointmentId, service = Depends(get_appointment_service)):
    return await service.get_id_by_data(appointment_data)


@router.post(
    "/service_id",
    status_code=status.HTTP_200_OK,
    summary="Получить ID по данным услуги"
)
async def get_id_by_service_data(service_data: ServiceId, service = Depends(get_service_service)):
    return await service.get_service_id_by_service_data(service_data)


@router.post(
    "/master_id",
    status_code=status.HTTP_200_OK,
    summary="Получить ID по данным мастера"
)
async def get_id_by_master_data(master_data: MasterId, service = Depends(get_master_service)):
    return await service.get_master_id_by_master_data(master_data)


@router.post(
    "/client_id",
    status_code=status.HTTP_200_OK,
    summary="Получить ID по данным клиента"
)
async def get_id_by_tg_id(tg_id: str, service = Depends(get_client_service)):
    return await service.get_client_id_by_tg_id(tg_id)