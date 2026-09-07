from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.schemas import Receipt
from src.db.main import get_session
from src.db.repository import TransactionRepository
from src.service import TransactionService


receiptrouter = APIRouter()


@receiptrouter.post("/verify_receipt")
async def receive_receipt(
    receipt_data: Receipt,
    session: AsyncSession = Depends(get_session),
):
    repository = TransactionRepository(session)
    service = TransactionService(repository)

    return await service.verify(receipt_data)

@receiptrouter.post("/vereify_link")
async def receive_link():
    continue