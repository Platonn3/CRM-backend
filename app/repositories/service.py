from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Service as ServiceModel


class ServiceRepository(BaseRepository[ServiceModel]):
    async def get_by_info(self, name: str, description: str, default_price: int) -> ServiceModel | None:
        query = (select(self.model)
                 .where(self.model.name == name,
                        self.model.description == description,
                        self.model.default_price == default_price))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()