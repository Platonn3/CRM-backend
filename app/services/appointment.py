from app.repositories.appointment import AppointmentRepository
from app.repositories.client import ClientRepository
from app.repositories.master import MasterRepository
from app.repositories.service import ServiceRepository
from app.schemas.appointment import AppointmentCreate, AppointmentId

from fastapi import HTTPException, status


class AppointmentService:
    def __init__(self, client_repo: ClientRepository, master_repo: MasterRepository, service_repo: ServiceRepository, appointment_repo: AppointmentRepository):
        self.master_repo = master_repo
        self.service_repo = service_repo
        self.appointment_repo = appointment_repo
        self.client_repo = client_repo

    async def get_id_by_data(self, appointment_data: AppointmentId):
        appointment = await self.appointment_repo.find_existing_slot(**appointment_data.model_dump())
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Записи yt существует"
            )
        return appointment.id

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
            **appointment_data.model_dump()
        )

    async def book_slot(self, client_id: int, appointment_id: int):
        appointment = await self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Записи не существует")
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Клиент не найден")

        if appointment.client_id > 0:
            if appointment.client_id == client_id:
                raise HTTPException(status_code=400, detail="Вы уже записаны")
            raise HTTPException(status_code=400, detail="Слот занят")

        appointment.client_id = client_id
        await self.appointment_repo.db.commit()
        await self.appointment_repo.db.refresh(appointment)
        return appointment

    async def unlink_client_from_appointment(self, client_id, appointment_id: int):
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиента с таким ID не существует")
        appointment = await self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Записи с таким ID не существует")
        if appointment.client_id == client_id:
            appointment.client_id = 0
            await self.appointment_repo.db.commit()
            await self.appointment_repo.db.refresh(appointment)
            return appointment
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отмена невозможна, клиент не записан на эту услугу")

    async def delete_appointment(self, appointment_id):
        appointment = await self.appointment_repo.delete(appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Услуги не существует")
        return appointment

    async def get_clients_appointments(self, client_id):
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиента с таким ID не существует")
        return await self.appointment_repo.get_clients_appointments(client_id)