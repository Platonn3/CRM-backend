from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connect import config
from app.database.models import Base

from fastapi import HTTPException


async def get_model_by_id_or_404(id: int, model, db: AsyncSession):
    result = await db.execute(select(model).where(model.id == id))
    result_model = result.scalar_one_or_none()

    if not result_model:
        raise HTTPException(status_code=404, detail=f"{model.__name__} не существует")

    return result_model
