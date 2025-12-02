from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Appointment as AppointmentModel


class AppointmentRepository(BaseRepository[AppointmentModel]):
    async def find_existing_slot(
            self,
            date, start_time, finish_time, master_id
    ) -> AppointmentModel | None:
        query = select(self.model).where(
            and_(
                self.model.master_id == master_id,
                self.model.date == date,
                self.model.start_time < finish_time,
                self.model.finish_time > start_time
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()