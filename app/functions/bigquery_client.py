import os
import logging
from google.cloud import bigquery
from google.oauth2 import service_account
from functions import data_processing
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de .env
load_dotenv()

# Constantes
SCOPES = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/drive"]
PROJECT = os.getenv("PROJECT")
DATASET = os.getenv("DATASET")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# Configurar logging
logging.basicConfig(level=logging.INFO)

# ====================================================================
#                                 Functions
# ====================================================================

def get_bigquery_client():
    
    """ Função para retornar o cliente BigQuery com as credenciais """
    
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"], 
        scopes=SCOPES
    )
    return bigquery.Client(credentials=credentials)

def gravar_tags(df_nova_tag, nome_trilha):
    
    """ Grava as tags no BigQuery"""
    
    try:
        # client BigQuery
        client = get_bigquery_client()

        # define table name and id
        table_name = f"tb_tags_{nome_trilha}"
        table_id = f"{PROJECT}.{DATASET}.{table_name}"

        job_config = bigquery.job.LoadJobConfig()

        # set write_disposition parameter as WRITE_APPEND for appending to table
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

        job = client.load_table_from_dataframe(df_nova_tag, table_id, job_config=job_config)

        job.result()  # Wait for the job to complete.

        table = client.get_table(table_id)  # Make an API request.
        
        logging.info("Loaded %s rows and %s columns to %s", table.num_rows, len(table.schema), table_id)
    
    except Exception as e:
        logging.error(f"Erro ao gravar tags no BigQuery: {e}")
        raise

def carregar_tags(trilha):
   
    """ Carrega as tags do BigQuery para acesso na API da Cademi """
   
    # client BigQuery
    client = get_bigquery_client()

    # consulta no BigQuery
    QUERY = f"select * from nome_tabela_{trilha}"
    query_job = client.query(QUERY)

    # converter para dataframe
    df_raw = query_job.to_dataframe()

    return df_raw

def carregar_dados(trilha):
    
    """ Carrega os dados de progresso do BigQuery e retorna um dataframe tratado. """
    
    # client BigQuery
    client = get_bigquery_client()

    # consulta no BigQuery
    QUERY = f"select * from nome_tabela_{trilha}"
    query_job = client.query(QUERY)

    # converter para dataframe
    df_raw = query_job.to_dataframe()
    
    # Limpar o código
    df1 = data_processing.data_clean(df_raw, trilha)

    return df1