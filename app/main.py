from fastapi import FastAPI
from app.api.v1.clients import router as clients_router
app = FastAPI(
    title="Beauty Salon API",
    version="1.0.0",
    description="API для салона красоты"
)

app.include_router(clients_router, prefix="/api/v1")