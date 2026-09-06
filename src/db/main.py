from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import config
from src.db.models import receipt 
from sqlalchemy.ext.asyncio.session import AsyncSession

engine = create_async_engine(
    url = config.DB_URL,
    echo = True
    # what is echo???
)

async def connect_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session