from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from db_connection import get_db_session
from models import Pedido
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Definindo o esquema Pydantic para a resposta
class PedidoResponse(BaseModel):
    pedido: str
    data_pedido: str
    pedido_externo: str
    pedido_cliente: str
    tipo_pedido: str
    filial: str
    canal: str
    cod_cliente: str
    transportadora: str
    moeda: str
    tot_valor_original: float
    tot_valor_entregue: float
    tot_valor_cancelado: float
    desconto: float

    class Config:
        orm_mode = True

@app.get("/pedidos", response_model=List[PedidoResponse])
async def get_pedidos():
    try:
        db: Session = get_db_session()
        pedidos = db.query(Pedido).limit(50).all()
        db.close()
        return pedidos
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=str(e))
