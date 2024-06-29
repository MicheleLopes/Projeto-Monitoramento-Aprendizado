#IMPORTS    
import configs
import logging
import json
import pandas as pd
from tqdm import tqdm
import requests
import time
import os
import phonenumbers
import unicodedata
from google.cloud import bigquery
from google.oauth2 import service_account

# Constantes
SCOPES = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/drive"]

# Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "token/credenciais.json"

# Configurar logging
logging.basicConfig(level=logging.INFO)


dir_path = os.path.dirname(os.path.realpath(__file__))

def extrair_alunos_tags(tag_ids,tabela):

    """ Função para extrair os alunos de acordo com as tags fornecidas """

    api_key = configs.get_cademi_api_keys()
    url_usuarios_base = configs.get_cademi_usuarios_base_url()

    headers = {
        "Accept": "application/json",
        "Authorization": api_key,
    }

    df_final = pd.DataFrame()

    client = get_bigquery_client()

    for tag_id in tag_ids:
        endpoint = f"/usuario/lista_por_tag/{tag_id}"
        url = url_usuarios_base + endpoint

        emails = set()
        nomes = set()
        celular = set()
        page = 1

        while url:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()
            resposta_json = resposta.json()

            # Se não há mais dados, saia do loop
            if not resposta_json['data']['usuario']:
                break

            # extrair emails nome e celulares dos alunos
            emails = [usuario['email'] for usuario in resposta_json['data']['usuario']]
            
            # extrair nome dos alunos de acordo com email
            nomes = [usuario['nome'] for usuario in resposta_json['data']['usuario']]
            
            #extrair celular dos alunos de acordo com email
            celular = [usuario['celular'] for usuario in resposta_json['data']['usuario']]

            # Atualizar a URL para a próxima página
            url = resposta_json['data']['paginator']['next_page_url']

            # Imprimir a página atual
            print(f"Extraindo dados da página {page} da tag {tag_id}...")
            page += 1

        # criar dataframe com emails e nomes e celulares
        df = pd.DataFrame({'email': list(emails), 'nome': list(nomes), 'celular': list(celular)})
        
        # remover duplicados
        df = df.drop_duplicates(subset=['email'])
        
        # criar coluna com tag_id
        df['turma'] = tag_id
        
        # ler dados da tabela BigQuery
        query = f"SELECT * FROM `{PROJECT}.{DATASET}.{tabela}`"
        aux = client.query(query).to_dataframe()

        # substituir valores da coluna turma pela coluna nome do arquivo tags_analista.csv
        df['turma'] = df['turma'].replace(aux.set_index('id')['nome'].to_dict()) 
        
        # Adicionar ao DataFrame final
        df_final = pd.concat([df_final, df])

    return df_final

def feature_engineering(df):

    """ Função para realizar feature engineering no DataFrame"""
    
    #remover % da coluna progresso_do_aluno
    df = df.replace('%', '', regex=True)

    #fill na
    df.fillna(0, inplace=True)

    # change type
    df['progresso_do_aluno'] = df['progresso_do_aluno'].astype('float64')

    # collection_date
    df['collection_date'] = df['collection_date'].astype('datetime64[ns]').dt.floor('d')
    
    # Ordena o DataFrame
    df = df.sort_values(by=['aluno_email', 'collection_date'])
    
    # Add número da semana do ano correspondente
    df['semana_ano'] = df['collection_date'].dt.isocalendar().week
    df = df.drop(columns=['collection_date'])
    
    return df

def formatar_celular(numero_cel):

    """ Função para formatar o número de celular"""

    try:
        numero_cel = phonenumbers.parse(numero_cel, "BR")
        return phonenumbers.format_number(numero_cel, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except Exception as e:
        return numero_cel

def remover_acentos(input_str):

    """ Função para remover acentos de uma string"""

    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()

def criar_dataframe_final(df1, df2):

    """ Função para criar o DataFrame final"""
    
    #juntar os datasets pela informação do e-mail
    df = pd.merge(df1, df2, left_on='aluno_email', right_on='email', how='left')
    
    #Aqui df1 seria os dados com o progresso e df2 seria a tabela que contém o nome e telefone
    df = df.drop('email', axis=1)

    #alterar padrao numero celular
    df['celular'] = df['celular'].apply(formatar_celular)

    # normalizar texto colunas 'nome' e 'nome_produto'
    df['nome'] = df['nome'].map(remover_acentos).str.strip()
    df['nome_produto'] = df['nome_produto'].map(remover_acentos).str.strip()

    #reordenar colunas
    df = df[['aluno_email', 'nome', 'celular', 'produto_id', 'nome_produto', 'progresso_do_aluno', 'semana_ano', 'turma']]

    logging.info("Dataframe final criado com sucesso!")

    return df

def get_progresso_aluno_por_produto(lista_alunos, lista_produtos, nome_trilha):

    """ Função para obter o progresso do aluno por produto"""
    
    api_key = configs.get_cademi_api_keys()
    url_usuarios_base = configs.get_cademi_usuarios_base_url()

    headers = {
        "Accept": "application/json",
        "Authorization": api_key,
    }

    lista_emails_alunos = lista_alunos
    lista_produtos_id = lista_produtos

    # Converta o campo 'id' para inteiro
    for produto in lista_produtos_id:
        produto['id'] = int(produto['id'])    

    df_progresso_alunos = pd.DataFrame()

    for email_aluno in tqdm(lista_emails_alunos):
      for produto in tqdm(lista_produtos_id):
        try:
            # Construa a URL usando f-strings
            endpoint = f"/usuario/progresso_por_produto/{email_aluno['email']}/{produto['id']}"
            url = url_usuarios_base + endpoint

            # Envolva a chamada da API em um bloco try-except
            try:
                resposta = requests.get(url, headers=headers)
                resposta.raise_for_status()  # Gera uma exceção para códigos de erro HTTP

                resposta_json = resposta.json()

                # Verifique se há dados na resposta
                if resposta_json.get("data") and resposta_json["data"].get("progresso") and resposta_json["data"]["progresso"].get("total"):
                    progresso_do_aluno = resposta_json["data"]["progresso"]["total"]

                    # Construa um dicionário para criar o DataFrame
                    data = {
                        'aluno_email': [email_aluno['email']],
                        'produto_id': [produto['id']],
                        'nome_produto': produto['nome'],
                        'progresso_do_aluno': [progresso_do_aluno]
                    }

                    # Use pd.DataFrame() diretamente sem a necessidade de concatenação
                    data = pd.DataFrame(data)
                    df_progresso_alunos = pd.concat([df_progresso_alunos, data], axis=0)

            except requests.exceptions.RequestException as err:
                print(f"Request Error: {err}")

            time.sleep(0.8)  # Espera o tempo necessário para respeitar o limite da API 

        except Exception as e:
            print(f"Error: {e}")
    
    return df_progresso_alunos

def get_bigquery_client():
    
    """ Função para retornar o cliente BigQuery com as credenciais """
    
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"], 
        scopes=SCOPES
    )
    return bigquery.Client(credentials=credentials)

def gravar_progresso(lista_progresso_alunos, trilha):
    
    """ Grava progresso no BigQuery"""
    
    # client BigQuery
    client = get_bigquery_client()

    logging.info("Enviando dados para o BigQuery...")

    # define table name and id
    table_name = f"tb_progresso_turmas_{trilha}"
    table_id = f"{PROJECT}.{DATASET}.{table_name}"

    job_config = bigquery.job.LoadJobConfig()

    # set write_disposition parameter as WRITE_APPEND for appending to table
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    job = client.load_table_from_dataframe(lista_progresso_alunos, table_id, job_config=job_config)

    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    
    logging.info("Loaded %s rows and %s columns to %s", table.num_rows, len(table.schema), table_id)
    
    logging.info("Carga finalizada!")

def read_table(tabela):
        
    """ Função para ler uma tabela do BigQuery"""

    client = get_bigquery_client()
    query = f"SELECT * FROM {PROJECT}.{DATASET}.{tabela}"
    df = client.query(query).to_dataframe()
    return df

def extract_tags(df, tabela):

    """ Função para extrair tags de alunos"""

    tag_ids = df['id'].values.tolist()
    return extrair_alunos_tags(tag_ids, tabela)

def create_paths(df, products):

    """ Função para criar os caminhos dos arquivos"""
    
    return [{'email': email} for email in df['email']], products[['id', 'nome']].to_dict(orient='records')