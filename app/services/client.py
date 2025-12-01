from fastapi import HTTPException, status
from app.repositories.client import ClientRepository
from app.schemas.client import ClientCreate


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def create_client(self, client_data: ClientCreate):
        existing_client = await self.client_repo.get_by_phone_or_tg_id(
            phone=client_data.phone,
            tg_id=client_data.tg_id
        )

        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Клиент с таким телефоном или Telegram ID уже существует"
            )

        return await self.client_repo.create(**client_data.model_dump())

    async def get_all_clients(self):
        clients = await self.client_repo.get_all()
        return [client for client in clients if client.id != 0]

    async def get_client_by_tg_id(self, tg_id: str):
        client = await self.client_repo.get_by_tg_id(tg_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не найден"
            )
        return client

    async def get_client_by_id(self, client_id: int):
        client = await self.client_repo.get_by_id(client_id)
        if not client or client.id == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не найден"
            )
        return client