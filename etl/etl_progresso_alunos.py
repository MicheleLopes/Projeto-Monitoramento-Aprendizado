# IMPORTS
from datetime import datetime
from create_dataframe import  get_progresso_aluno_por_produto, feature_engineering, criar_dataframe_final, gravar_progresso, read_table, extrair_alunos_tags, extract_tags, create_paths

# ==================================================================================
#                                 Create Paths
# ==================================================================================
 # tags - analista
tags_analista = read_table('nome_tabela')
df_analista = extract_tags(tags_analista, 'nome_tabela')

# tags - cientista
tags_cientista = read_table('nome_tabela')
df_cientista = extract_tags(tags_cientista, 'nome_tabela')

# produtos
produtos_analista = read_table('nome_tabela')
produtos_cientista = read_table('nome_tabela')

# path
PATH_USER_AD, PATH_PROD_AD = create_paths(df_analista, produtos_analista)
PATH_USER_CD, PATH_PROD_CD = create_paths(df_cientista, produtos_cientista)


# ==================================================================================
#                                ETL Progresso Alunos
# ==================================================================================

def etl_api_cademi(df, lista_alunos, lista_produtos, trilha):
    
    lista_progresso_alunos = get_progresso_aluno_por_produto(lista_alunos=lista_alunos, lista_produtos=lista_produtos, nome_trilha=trilha)
    lista_progresso_alunos["collection_date"] = datetime.now()
    lista_progresso_alunos = feature_engineering(lista_progresso_alunos)
    lista_progresso_alunos = criar_dataframe_final(lista_progresso_alunos,df)
    gravar_progresso(lista_progresso_alunos, trilha)

# ==================================================================================
#                                       Main
# ==================================================================================

print("Chamando etl_api_cademi para analista...")
etl_api_cademi(df_analista, lista_alunos=PATH_USER_AD, lista_produtos=PATH_PROD_AD, trilha='analista')

print("Chamando etl_api_cademi para cientista...")
etl_api_cademi(df_cientista, lista_alunos=PATH_USER_CD, lista_produtos=PATH_PROD_CD, trilha='cientista')
