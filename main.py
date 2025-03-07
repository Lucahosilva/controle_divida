from fastapi import FastAPI, status
from datetime import datetime
import uuid
import pytz

from src.databases.database import Database
from src.routers.health_check import health_router
from src.models.transaction_model import Transaction
from src.utils.logger import logger
from src.models.response_models import TransactionOut

collection = Database()._connect()

app = FastAPI()
app.include_router(health_router)


@app.post("/create", status_code=status.HTTP_201_CREATED, response_model=TransactionOut)
def create_transaction(payload: dict):

    payload["_id"] = str(uuid.uuid4())
    payload["ultima_atualizacao"] = datetime.now(
        tz=pytz.timezone("America/Sao_Paulo")
    )
    transaction = Transaction(**payload)

    logger.info(f"Creating transaction")

    collection.insert_one(transaction.model_dump(by_alias=True))
    return {"message": "Transação criada com sucesso", "id":transaction.id}


@app.get("/total")
def total():

    total = 0
    for transaction in collection.find():
        total += transaction["value"]

    return {"valor_original": 70000, "valor_pago": total, "Restante": 70000 - total}


@app.delete(
    "/delete/{transaction_id}",
    status_code=status.HTTP_200_OK,
)
def delete_transaction(transaction_id: str):

    result = collection.delete_one({"_id": transaction_id})
    if result.deleted_count == 0:
        return {"message": "Transação não encontrada"}, 404

    return {"message": "Transação deletada com sucesso"}


@app.put("/update/{transaction_id}")
def update_transaction(transaction_id: str, new_transaction: dict):

    transaction = collection.find_one({"_id": transaction_id})
    if not transaction:
        return {"message": "Transação não encontrada"}, 404

    for key, value in new_transaction.items():

        if key == "payment_date":
            value = datetime.strptime(value, "%Y-%m-%d")

        transaction[key] = value

    transaction["ultima_atualizacao"] = datetime.now(
        tz=pytz.timezone("America/Sao_Paulo")
    )

    collection.update_one({"_id": transaction_id}, {"$set": transaction})
    return {"message": "Transação atualizada com sucesso"}, 200


@app.get("/list")
def list_transactions():

    transactions = []
    for transaction in collection.find():
        transaction["_id"] = str(transaction["_id"])
        transaction["payment_date"] = transaction["payment_date"].strftime("%Y-%m-%d")
        transaction["ultima_atualizacao"] = transaction["ultima_atualizacao"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        transactions.append(transaction)

    return {"transactions": transactions}
