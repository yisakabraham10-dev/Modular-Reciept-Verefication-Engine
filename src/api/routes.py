from fastapi import APIRouter, status
from src.api.schemas import Receipt

receiptrouter = APIRouter()

@receiptrouter.post("/verify_receipt", status_code= status.HTTP_201_CREATED)
async def receinved_receipt(receipt: Receipt):
    
    received_receipt = receipt.model_dump()