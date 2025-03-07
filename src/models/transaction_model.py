from pydantic import BaseModel, Field
from datetime import datetime


class Transaction(BaseModel):
    id: str = Field(..., alias="_id")
    value: float
    payment_date: str
    account: str
    receipt_link: str
    obs: str
    ultima_atualizacao: datetime
