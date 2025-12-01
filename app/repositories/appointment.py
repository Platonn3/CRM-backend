from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Appointment as AppointmentModel


class AppointmentRepository(BaseRepository[AppointmentModel]):
    async def find_existing_slot(
            self,
            date, start_time, end_time, master_id
    ) -> AppointmentModel | None:
        query = (select(AppointmentModel)
                 .where(AppointmentModel.date == date,
                        AppointmentModel.start_time == start_time,
                        AppointmentModel.finish_time == end_time,
                        AppointmentModel.master_id == master_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()