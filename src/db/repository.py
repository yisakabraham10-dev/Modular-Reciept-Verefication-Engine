from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import receipt


class TransactionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_reference(self, reference: str):
        statement = select(receipt).where(
            receipt.transaction_reference == reference
        )

        result = await self.session.exec(statement)

        return result.first()

    async def create(self, transaction: receipt):
        self.session.add(transaction)

        await self.session.commit()
        await self.session.refresh(transaction)

        return transaction