import uvicorn
from fastapi import FastAPI
from app.api.v1.clients import router as clients_router
from app.api.v1.admin import router as admin_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Beauty Salon API",
    version="1.0.0",
    description="API для салона красоты"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(clients_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app)