from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connect import config
from app.schemas.client import ClientCreate, ClientResponse
from app.database.models import Client as ClientModel

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
    result = await db.execute(select(ClientModel))
    clients = result.scalars().all()
    return clients


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Получить клиента по ID"
)
async def get_client_by_id(
    client_id: int,
    db: AsyncSession = Depends(config.get_db)
):
    client = await db.get(ClientModel, client_id)
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Клиент не найден"
        )
    return client