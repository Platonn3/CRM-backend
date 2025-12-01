from app.repositories.appointment import AppointmentRepository
from app.repositories.master import MasterRepository
from app.repositories.service import ServiceRepository
from app.schemas.appointment import AppointmentCreate

from fastapi import HTTPException, status


class AppointmentService:
    def __init__(self, master_repo: MasterRepository, service_repo: ServiceRepository, appointment_repo: AppointmentRepository):
        self.master_repo = master_repo
        self.service_repo = service_repo
        self.appointment_repo = appointment_repo

    async def create_slot(self, appointment_data: AppointmentCreate):
        appointment = await self.appointment_repo.find_existing_slot(
            appointment_data.date,
            appointment_data.start_time,
            appointment_data.finish_time,
            appointment_data.master_id
        )
        if appointment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Запись уже существует"
            )
        master = await self.master_repo.get_by_id(appointment_data.master_id)
        if not master:
            raise HTTPException(status_code=404, detail="Maстер не существует")
        service = await self.service_repo.get_by_id(appointment_data.service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Услуга не существует")
        return await self.appointment_repo.create(
            **appointment_data.model_dump(),
        )