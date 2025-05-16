import os
import openai
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar a API da OpenAI
openai.api_key = OPENAI_API_KEY


def generate_gpt_response(prompt: str, model: str = "gpt-4") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente de IA que responde com base nos dados do DW."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        # Retorna apenas o conteúdo da resposta
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar resposta do ChatGPT: {e}")
        return "Erro ao gerar resposta. Verifique a conexão e a chave da API."

# chat_integration.py (Adicione no final do arquivo)
import requests

def get_total_vendas(year=2023):
    try:
        response = requests.get(f"http://localhost:8000/vendas_total")
        response.raise_for_status()
        data = response.json()
        return f"Total de vendas em {year}: R$ {data['total_vendas']:.2f} com {data['total_pedidos']} pedidos."
    except Exception as e:
        return f"Erro ao buscar total de vendas: {e}"
