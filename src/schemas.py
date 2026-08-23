from fastapi import APIRouter, status
from src.routes import Receipt

receiptrouter = APIRouter()

@receiptrouter.post("/verify_receipt", status_code= status.HTTP_201_CREATED)
async def receinved_receipt(receipt: Receipt):
    
    received_receipt = receipt.model_dump()
