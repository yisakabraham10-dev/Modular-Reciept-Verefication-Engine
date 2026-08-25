from fastapi import APIRouter, status
from src.api.schemas import Receipt
from src.core_logic.verifier import verifier

receiptrouter = APIRouter()

@receiptrouter.post("/verify_receipt", status_code= status.HTTP_201_CREATED)
async def receinved_receipt(receipt: Receipt):

    result = verifier(receipt)

    if result:
        return{"message": "verified"}
    if not result:
        return {"message": "transaction not verified!!!"}