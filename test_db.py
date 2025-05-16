from db_connection import get_db

def test_connection():
    try:
        db = next(get_db())
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    test_connection()
