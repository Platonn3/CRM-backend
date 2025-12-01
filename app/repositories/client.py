from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Client as ClientModel


class ClientRepository(BaseRepository[ClientModel]):
    async def get_by_phone_or_tg_id(self, phone: str, tg_id: str | None) -> ClientModel | None:
        query = select(self.model).where(
            or_(
                self.model.phone == phone,
                self.model.tg_id == tg_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_tg_id(self, tg_id: str) -> ClientModel | None:
        query = select(self.model).where(self.model.tg_id == tg_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()