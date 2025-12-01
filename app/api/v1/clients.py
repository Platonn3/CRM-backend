from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.extensions import get_model_by_id_or_404
from app.database.connect import config
from app.schemas.client import ClientCreate, ClientResponse
from app.schemas.master import MasterResponse, MasterWithServices, MasterWithAppointments
from app.schemas.service import ServiceResponse
from app.schemas.appointment import AppointmentResponse
from app.database.models import Client as ClientModel
from app.database.models import Master as MasterModel
from app.database.models import Service as ServiceModel
from app.database.models import Appointment as AppointmentModel

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового клиента"
)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(config.get_db)
):
    existing_client = await db.execute(
        select(ClientModel).where(
            (ClientModel.phone == client_data.phone) |
            (ClientModel.tg_id == client_data.tg_id)
        )
    )
    if existing_client.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Клиент с таким телефоном или Telegram ID уже существует"
        )

    new_client = ClientModel(
        name=client_data.name,
        surname=client_data.surname,
        phone=client_data.phone,
        tg_id=client_data.tg_id
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)

    return new_client


@router.get(
    path="/",
    response_model=list[ClientResponse],
    summary="Получить всех клиентов"
)
async def get_all_clients(db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(select(ClientModel).where(ClientModel.id != 0))
    clients = result.scalars().all()
    return clients


@router.get(
    "/by_tg/{tg_id}",
    response_model=ClientResponse,
    summary="Получить клиента по tg_id"
)
async def get_client_by_tg_id(tg_id: str, db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(
        select(ClientModel)
        .where(ClientModel.tg_id == tg_id)
    )
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Клиент не найден"
        )
    return client


@router.get(
    "/masters",
    response_model=list[MasterResponse],
    summary="Получить всех мастеров"
)
async def get_all_masters(db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(select(MasterModel))
    masters = result.scalars().all()
    return masters


@router.get(
    "/masters/{id}",
    response_model=MasterResponse,
    summary="Получить мастера по id"
)
async def get_master_by_id(id: int, db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(
        select(MasterModel)
        .where(MasterModel.id == id)
    )
    master = result.scalars().one_or_none()
    if not master:
        raise HTTPException(
            status_code=404,
            detail="Мастер не найден"
        )
    return master


@router.get(
    "/masters/{master_id}/services",
    response_model=MasterWithServices,
    status_code=status.HTTP_200_OK,
    summary="Получить все услуги мастера"
)
async def get_master_with_services(master_id: int, db: AsyncSession = Depends(config.get_db)):
    master_request = await db.execute(
        select(MasterModel)
        .options(selectinload(MasterModel.services))
        .where(MasterModel.id == master_id)
    )
    master = master_request.scalar_one_or_none()
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мастер не существует"
        )

    return master


@router.get(
    "/services",
    response_model=list[ServiceResponse],
    summary="Получить все виды услуг"
)
async def get_all_services(db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(select(ServiceModel))
    services = result.scalars().all()
    return services


@router.get(
    "/services/{id}",
    response_model=ServiceResponse,
    summary="Получить услугу по id"
)
async def get_all_services(id: int, db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(
        select(ServiceModel)
        .where(ServiceModel.id == id)
    )
    service = result.scalars().one_or_none()
    if not service:
        raise HTTPException(
            status_code=404,
            detail="Услуга не найдена"
        )
    return service


@router.get(
    "/appointments",
    response_model=list[AppointmentResponse],
    summary="Получить все записи"
)
async def get_all_appointments(db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(select(AppointmentModel))
    appointment = result.scalars().all()
    return appointment


@router.post(
    path="/{client_id}/appointments/{appointment_id}",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Записать клиента на услугу"
)
async def sign_up_client_on_appointment(client_id: int, appointment_id: int, db: AsyncSession = Depends(config.get_db)):
    await get_model_by_id_or_404(client_id, ClientModel, db)
    appointment = await get_model_by_id_or_404(appointment_id, AppointmentModel, db)

    if appointment.client_id > 0 and appointment.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Другой клиент записан на эту услугу")
    elif appointment.client_id > 0 and appointment.client_id == client_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Клиент уже записан на эту услугу")

    appointment.client_id = client_id
    await db.commit()
    await db.refresh(appointment)

    return appointment


@router.get(
    path="/masters/{master_id}/appointments",
    response_model=MasterWithAppointments,
    status_code=status.HTTP_200_OK,
    summary="Получить все услуги мастера"
)
async def get_masters_appointments(master_id: int, db: AsyncSession = Depends(config.get_db)):
    master_request = await db.execute(
        select(MasterModel)
        .options(selectinload(MasterModel.appointments))
        .where(MasterModel.id == master_id)
    )
    master = master_request.scalar_one_or_none()
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мастер не существует"
        )

    return master