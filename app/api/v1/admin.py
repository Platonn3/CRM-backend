from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Master as MasterModel, Service as ServiceModel, Appointment as AppointmentModel

from app.schemas.master import MasterResponse, MasterCreate

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