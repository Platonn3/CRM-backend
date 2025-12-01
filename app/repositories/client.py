from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.database.models import Client as ClientModel


class ClientRepository(BaseRepository[ClientModel]):
    pass