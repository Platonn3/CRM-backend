from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Service as ServiceModel


class ServiceRepository(BaseRepository[ServiceModel]):
    pass