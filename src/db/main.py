from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import config

engine = create_async_engine(
    url = config.DB_URL,
    echo = True
    # what is echo???
)

async def connect_db():
    async with engine.begin() as conn:
        statement  = text("SELECT 'hello'")

        result = await conn.execute(statement)

        print (result.all())
