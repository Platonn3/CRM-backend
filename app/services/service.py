from app.repositories.service import ServiceRepository

from fastapi import HTTPException, status

from app.schemas.service import ServiceId
from app.schemas.service import ServiceCreate


class ServiceService:
    def __init__(self, service_repo: ServiceRepository):
        self.service_repo = service_repo

    async def create_service(self, service_data: ServiceCreate):
        service = await self.service_repo.get_by_info(
            service_data.name,
            service_data.description,
            service_data.default_price
        )
        if service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Услуга уже существует"
            )
        return await self.service_repo.create(**service_data.model_dump())

    async def get_service(self, service_id):
        service = await self.service_repo.get_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Услуги не существует"
            )
        return service

    async def get_service_id_by_service_data(self, service_data: ServiceId):
        service = await self.service_repo.get_by_info(**service_data.model_dump())
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Услуги не существует"
            )
        return service.id

    async def get_all_services(self):
        return await self.service_repo.get_all()