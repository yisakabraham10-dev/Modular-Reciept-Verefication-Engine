from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config

engine = AsyncEngine(create_engine(
    url = config.DB_URL,
    echo = True
    # what is echo???
))