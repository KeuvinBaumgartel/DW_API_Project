from fastapi import FastAPI
from db_connection import get_db_session
from models import Pedido
from typing import List

app = FastAPI()

@app.get("/pedidos", response_model=List[Pedido])
async def get_pedidos():
    db = get_db_session()
    pedidos = db.query(Pedido).limit(50).all()
    return pedidos
