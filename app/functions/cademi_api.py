import logging
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de .env
load_dotenv()

# Constantes
CADEMI_API_URL = os.getenv("CADEMI_API_URL")
CADEMI_API_KEY = os.getenv("CADEMI_API_KEY")

# Configurar logging
logging.basicConfig(level=logging.INFO)

def get_tags():
    """ Função para acessar a API da Cademi e retornar os IDs das tags """

    headers = {
        "Accept": "application/json",
        "Authorization": CADEMI_API_KEY,
    }

    endpoint = f"/tag"
    url = CADEMI_API_URL + endpoint

    resposta = requests.get(url, headers=headers)
    if resposta.status_code == 200:
        # Converter a resposta em um objeto Python
        data = resposta.json()

        # Extrair os IDs dos itens e guardar em uma lista
        ids = [item['id'] for item in data['data']['itens']]
    else:
        logging.error("Erro ao acessar a API: %s", resposta.status_code)
    
    return ids
