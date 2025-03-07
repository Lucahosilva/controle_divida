from pydantic import BaseModel

class TransactionOut(BaseModel):
    message: str
    id: str
