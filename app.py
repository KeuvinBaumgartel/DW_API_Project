# app.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connection import get_db
from models import Pedido
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PedidoResponse(BaseModel):
    pedido: str
    data_pedido: Optional[str] = None
    pedido_externo: Optional[str] = None
    pedido_cliente: Optional[str] = None
    tipo_pedido: Optional[str] = None
    filial: Optional[str] = None
    canal: Optional[str] = None
    cod_cliente: Optional[str] = None
    transportadora: Optional[str] = None
    moeda: Optional[str] = None
    cod_tab_preco: Optional[str] = None
    colecao_pedido: Optional[str] = None
    cod_representante: Optional[str] = None
    cod_gerente: Optional[str] = None
    natureza_saida: Optional[str] = None
    aprovacao: Optional[str] = None
    digitador: Optional[str] = None
    pedido_embarcado: Optional[str] = None
    data_ult_faturamento: Optional[str] = None
    origem_pedido: Optional[str] = None
    comissao_gerente: Optional[float] = None
    tot_qtde_original: Optional[int] = None
    tot_qtde_entregue: Optional[int] = None
    tot_qtde_cancelada: Optional[int] = None
    tot_qtde_entregar: Optional[int] = None
    tot_valor_original: Optional[float] = None
    tot_valor_entregue: Optional[float] = None
    tot_valor_cancelado: Optional[float] = None
    tot_valor_entregar: Optional[float] = None
    tot_bruto_entregue: Optional[float] = None
    valor_sub_itens: Optional[float] = None
    desconto: Optional[float] = None
    valor_desconto: Optional[float] = None
    desconto_bonificacao: Optional[float] = None
    desconto_digitado: Optional[float] = None
    desconto_extra: Optional[float] = None
    desconto_showroom_fisico: Optional[float] = None
    desconto_showroom_virtual: Optional[float] = None
    desconto_ltv: Optional[float] = None
    desconto_calculado: Optional[float] = None
    desconto_total: Optional[float] = None

    @validator("data_pedido", "data_ult_faturamento", pre=True, always=True)
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return value

    class Config:
        orm_mode = True


@app.get("/pedidos", response_model=List[PedidoResponse])
def get_pedidos(db: Session = Depends(get_db)):
    try:
        pedidos = db.query(Pedido).limit(50).all()
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedidos: {e}")


@app.get("/pedidos/{pedido}", response_model=PedidoResponse)
def get_pedido_by_id(pedido: str, db: Session = Depends(get_db)):
    try:
        pedido_obj = db.query(Pedido).filter(Pedido.pedido == pedido).first()
        if not pedido_obj:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        return pedido_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# app.py (Adicione no final do arquivo)
from fastapi import Body

@app.get("/vendas_total")
def get_vendas_total(db: Session = Depends(get_db)):
    try:
        result = db.execute("""
            SELECT 
                COUNT(pedido) AS total_pedidos,
                SUM(tot_valor_original) AS total_vendas
            FROM varejo.dim_pedidos
            WHERE EXTRACT(YEAR FROM data_pedido) = 2023
        """).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Nenhuma venda encontrada para 2023.")

        return {
            "total_pedidos": result.total_pedidos,
            "total_vendas": float(result.total_vendas) if result.total_vendas else 0.0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar total de vendas: {e}")
