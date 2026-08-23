from fastapi import APIRouter, status

receiptrouter = APIRouter()

@receiptrouter.post("/verify_receipt")
async def ()