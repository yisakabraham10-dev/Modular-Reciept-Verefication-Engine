from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

class receipt(SQLModel, table = True):
    __tablename__ = "receipts"


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    bank_type: str
    date_of_transaction: datetime = Field(default_factory=datetime.now)
    transaction_sender: str
    amount: Decimal
    transaction_reference: int
    transaction_type: str
    interfaced_at: datetime = Field(default_factory=datetime.now)
    transaction_receiver: str

    def __repr__(self):
        return f"<Receipt {self.transaction_reference }>"