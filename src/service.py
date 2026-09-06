from sqlmodel.ext.asyncio.session import AsyncSession
from .api.schemas import Receipt_Model
from .db.models import receipt
from sqlmodel import select

class transaction_methods:
    async def check_transaction(self, receiptschema: Receipt_Model, session: AsyncSession, transaction_reference: int):

        statement = select(receiptschema).where(receipt.transaction_reference)