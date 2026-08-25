from sqlmodel import SQLModel, Field, column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from uuid import UUID, uuid4

class db_schema(SQLModel, table = True):
    __tablename__ = "receipts"
    id: UUID = Field(sa_column= column(pg.UUID,
                                        nullable=False,
                                        primary_key = True,
                                        default= uuid4()))
    bank_type: str
    date_of_transaction: datetime = Field(column(pg.TIMESTAMP, 
                                                 default = datetime.now, 
                                                 nullable = False))
    transaction_sender: str
    amount: float
    transaction_reference: int
    transaction_type: str
    interfaced_at: datetime