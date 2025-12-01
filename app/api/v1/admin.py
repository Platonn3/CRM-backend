from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.extensions import get_model_by_id_or_404
from app.database.models import Master as MasterModel, Service as ServiceModel, Appointment as AppointmentModel, Client as ClientModel
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

from app.schemas.master import MasterResponse, MasterCreate, MasterWithServices

from app.database.connect import config
from app.schemas.service import ServiceResponse, ServiceCreate


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/masters",
    response_model=MasterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового мастера"
)
async def create_new_master(master_data: MasterCreate, db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(
        select(MasterModel).
        where(
            and_(
                MasterModel.name == master_data.name,
                MasterModel.surname == master_data.surname,
                MasterModel.phone == master_data.phone
            )
        )
    )
    master = result.scalar_one_or_none()

    if master:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Мастер с таким именем, фамилией и телефоном уже существует"
        )

    new_master = MasterModel(
        name=master_data.name,
        surname=master_data.surname,
        phone=master_data.phone
    )

    db.add(new_master)
    await db.commit()
    await db.refresh(new_master)

    return new_master


@router.post(
    "/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую услугу"
)
async def create_new_service(service_data: ServiceCreate, db: AsyncSession = Depends(config.get_db)):
    result = await db.execute(
        select(ServiceModel).
        where(
            and_(
                ServiceModel.name == service_data.name,
                ServiceModel.duration == service_data.duration,
                ServiceModel.description == service_data.description,
                ServiceModel.default_price == service_data.default_price
            )
        )
    )
    service = result.scalar_one_or_none()

    if service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Услуга уже существует"
        )

    new_service = ServiceModel(
        name=service_data.name,
        duration=service_data.duration,
        description=service_data.description,
        default_price=service_data.default_price
    )

    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)

    return new_service


@router.post(
    "/masters/{master_id}/services/{service_id}",
    response_model=MasterWithServices,
    status_code=status.HTTP_200_OK,
    summary="Добавить к мастеру услугу"
)
async def add_service_to_master(master_id: int, service_id: int, db: AsyncSession = Depends(config.get_db)):

    master_request = await db.execute(
        select(MasterModel)
        .where(MasterModel.id == master_id)
        .options(selectinload(MasterModel.services))
    )
    master = master_request.scalar_one_or_none()

    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мастер не существует"
        )

    service_request = await db.execute(
        select(ServiceModel)
        .where(ServiceModel.id == service_id)
    )
    service = service_request.scalar_one_or_none()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не существует"
        )

    if service in master.services:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Услуга уже есть у мастера"
        )

    master.services.append(service)

    await db.commit()
    await db.refresh(master, ["services"])

    return master


@router.post(
    "/appointments/masters/{master_id}/services/{service_id}",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую запись"
)
async def create_new_appointment(
    appointment_data: AppointmentCreate,
    master_id: int,
    service_id: int,
    db: AsyncSession = Depends(config.get_db)
):
    appointment_request = await db.execute(
        select(AppointmentModel).
        where(
            AppointmentModel.date == appointment_data.date,
            AppointmentModel.start_time == appointment_data.start_time,
            AppointmentModel.finish_time == appointment_data.finish_time,
            AppointmentModel.price == appointment_data.price,
            AppointmentModel.master_id == master_id,
            AppointmentModel.service_id == service_id,
        )
    )
    appointment = appointment_request.scalar_one_or_none()
    if appointment is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Запись уже существует"
        )

    await get_model_by_id_or_404(master_id, MasterModel, db)
    await get_model_by_id_or_404(service_id, ServiceModel, db)

    new_appointment = AppointmentModel(
        date=appointment_data.date,
        start_time=appointment_data.start_time,
        finish_time=appointment_data.finish_time,
        price=appointment_data.price,
        master_id=master_id,
        service_id=service_id,
        client_id=0
    )

    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)
    return new_appointment








