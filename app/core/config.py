from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.DATABASE_URL = (
            f"postgresql+psycopg://"
            f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        self.engine = create_async_engine(
            self.DATABASE_URL,
            echo=True,
            future=True,
            pool_size=5,
            max_overflow=10,
            connect_args={"sslmode": "require"},
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_db(self):
        async with self.AsyncSessionLocal() as session:
            yield session