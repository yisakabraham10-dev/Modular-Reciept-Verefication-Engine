from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID

class db_schema(SQLModel, table = True):
    id: UUID
    bank_type: str
    date_of_transaction: datetime
    transaction_sender: str
    amount: float
    transaction_reference: int
    transaction_type: str
    interfaced_at: datetime