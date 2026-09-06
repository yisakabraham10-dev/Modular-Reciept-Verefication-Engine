from src.api.schemas import Receipt
from src.db.models import receipt
from src.db.repository import TransactionRepository


class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def verify(self, receipt_data: Receipt):

        existing = await self.repository.get_by_reference(
            receipt_data.transaction_reference
        )

        if existing is not None:
            return {
                "status": "duplicate",
                "transaction_reference": receipt_data.transaction_reference,
            }

        transaction = receipt(
            bank_type=receipt_data.bank_type,
            date_of_transaction=receipt_data.date_of_transaction,
            transaction_sender=receipt_data.transaction_sender,
            amount=receipt_data.amount,
            transaction_reference=receipt_data.transaction_reference,
            transaction_type=receipt_data.transaction_type,
            transaction_receiver=receipt_data.transaction_receiver,
        )

        await self.repository.create(transaction)

        return {
            "status": "new",
            "transaction_reference": receipt_data.transaction_reference,
        }