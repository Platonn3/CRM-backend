from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository, ModelType
from app.database.models import Master as MasterModel


class MasterRepository(BaseRepository[MasterModel]):
    async def get_by_phone(self, master_phone: str) -> MasterModel| None:
        query = (select(self.model)
                 .where(self.model.phone == master_phone))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_services(self, master_id: int) -> MasterModel | None:
        query = ((select(self.model)
                 .options(selectinload(self.model.services)))
                 .where(self.model.id == master_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_appointments(self, master_id: int) -> MasterModel | None:
        query = ((select(self.model)
                 .options(selectinload(self.model.appointments)))
                 .where(self.model.id == master_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

