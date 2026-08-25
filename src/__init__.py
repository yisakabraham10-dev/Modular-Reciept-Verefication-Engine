from fastapi import FastAPI
from src.api.routes import receiptrouter
from contextlib import asynccontextmanager
from src.db.main import connect_db 

@asynccontextmanager
async def life_span(app: FastAPI):
    print ("server starting!!!") 
    await connect_db()
    yield
    print ("server session has ended")

version = "v1"
app = FastAPI(version=version, title="Modular receipt verefication engine", 
              description="first version will be a verifierapi that will just save and verify bank transactions from certain banks", 
              lifespan= life_span)

app.include_router(receiptrouter, prefix= '/test')