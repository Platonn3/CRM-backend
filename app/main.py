import uvicorn
from fastapi import FastAPI
from app.api.v1.clients import router as clients_router
from app.api.v1.admin import router as admin_router


app = FastAPI(
    title="Beauty Salon API",
    version="1.0.0",
    description="API для салона красоты"
)

app.include_router(clients_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app)