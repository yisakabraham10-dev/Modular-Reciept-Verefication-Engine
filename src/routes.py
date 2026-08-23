from pydantic import BaseModel
import datetime

class Receipt(BaseModel):
    bank_type: str
    date_of_transaction: datetime
    transaction_sender: str
    amount: float