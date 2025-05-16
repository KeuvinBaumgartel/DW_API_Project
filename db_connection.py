from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Carregando as variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configurando a engine e a sessão do banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
