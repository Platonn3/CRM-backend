from fastapi import HTTPException, status

from app.repositories.master import MasterRepository
from app.repositories.service import ServiceRepository
from app.schemas.master import MasterCreate


class MasterService:
    def __init__(self, master_repo: MasterRepository, service_repo: ServiceRepository):
        self.master_repo = master_repo
        self.service_repo = service_repo

    async def create_master(self, master_data: MasterCreate):
        master = await self.master_repo.get_by_phone(master_data.phone)
        if master:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Мастер с таким телефоном уже существует"
            )
        return await self.master_repo.create(**master_data.model_dump())

    async def add_service_to_master(self, master_id: int, service_id: int):
        master = await self.master_repo.get_with_services(master_id)
        if not master:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Мастер не существует"
            )
        service = await self.service_repo.get_by_id(service_id)
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
        await self.master_repo.db.commit()
        await self.master_repo.db.refresh(master)
        return master

    async def get_all_masters(self):
        return await self.master_repo.get_all()

    async def get_master_with_services(self, master_id: int):
        master = await self.master_repo.get_with_services(master_id)
        if not master:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Мастер не существует"
            )
        return master

    async def get_master_with_appointments(self, master_id: int):
        master = await self.master_repo.get_with_appointments(master_id)
        if not master:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Мастер не существует"
            )
        return master


