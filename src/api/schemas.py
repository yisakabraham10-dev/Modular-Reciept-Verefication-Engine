from pydantic import BaseModel
from datetime import datetime

class Receipt(BaseModel):
    bank_type: str
    date_of_transaction: datetime
    transaction_sender: str
    amount: float
    transaction_reference: int
    transaction_type: str
    transaction_receiver: str 
