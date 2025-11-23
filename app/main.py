from fastapi import FastAPI
from app.api.v1.clients import router as clients_router
from app.database.connect import Config

app = FastAPI(
    title="Beauty Salon API",
    version="1.0.0",
    description="API для салона красоты"
)
config = Config()

app.include_router(clients_router, prefix="/api/v1")