from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config

engine = AsyncEngine(create_engine(
    url = config.DB_URL,
    echo = True
    # what is echo???
))

async def connect_db():
    async with engine.begin() as conn:
        statement  = text("SELECT 'hello'")

        result = await conn.execute(statement)

        print (result.all())
