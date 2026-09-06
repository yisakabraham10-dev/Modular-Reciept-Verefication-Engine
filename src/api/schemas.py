from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class Receipt(BaseModel):
    bank_type: str
    date_of_transaction: datetime
    transaction_sender: str
    amount: Decimal
    transaction_reference: str
    transaction_type: str
    transaction_receiver: str