from fastapi import FastAPI
from sqlalchemy.orm import Session
from db_connection import get_db
from models import Pedido
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Habilitando CORS para permitir conexões externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pedidos", response_model=List[Pedido])
def get_pedidos(db: Session = get_db()):
    try:
        pedidos = db.query(Pedido).limit(50).all()
        return pedidos
    except Exception as e:
        return {"error": f"Erro ao buscar pedidos: {str(e)}"}
