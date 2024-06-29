import streamlit as st
import io
import base64
import numpy as np
import pandas as pd
from functions import bigquery_client
from functions import cademi_api 

def processar_inputs(nova_tag, numero_turma, adicionar, nome_trilha):
    
    """" Função para processar as entradas do usuário e adicionar a nova tag na tabela de tags """
    
    # Carregar tags existentes
    df = bigquery_client.carregar_tags(nome_trilha)
    tag_id = df['id'].values.tolist()
    tag_lista = df.set_index('id')['nome'].to_dict()   

    texto = ""
    if adicionar:
        lista_tags = cademi_api.get_tags()
        # Verificar se ambos são apenas dígitos
        if numero_turma.isdigit() and nova_tag.isdigit():
            # Verificar se a tag existe na cademi
            if int(nova_tag) in lista_tags:
                # Verificar se a tag já existe na tabela
                if int(nova_tag) in tag_id:
                    texto = "Tag informada já existe"
                else:
                    nome_turma = f'turma {numero_turma}'
                    # Verificar se o número da turma já existe na tabela
                    if nome_turma in tag_lista.values():
                        texto = "Turma informada já existe"
                    else:
                        # Adicionar o par de número e turma ao dicionário tag_lista
                        tag_id.append(nova_tag)
                        tag_lista[nova_tag] = nome_turma
                        texto = "Tag adicionada com sucesso para as próximas coletas."
                        df = pd.DataFrame(list(tag_lista.items()), columns=['id', 'nome'])
                        df['id'] = df['id'].astype(int)
                        bigquery_client.gravar_tags(df, nome_trilha)
            else:
                texto = "Tag não encontrada na Cademi."
        else:
            texto = "Por favor insira apenas números inteiros."
    # Salvar as informações atualizadas de volta no arquivo CSV
    return st.markdown(texto)  

def calcular_kpis(df, cursos):
        
    """" Função para calcular total de alunos, total de turmas e média de progresso """

    # alunos únicos
    total_alunos = df['aluno_email'].nunique()
    
    # turmas únicas
    total_turmas = df['turma'].nunique()
    
    # média de progresso (métrica de acompanhamento)
    media_progresso = df[cursos].mean().mean()
    
    return total_alunos, total_turmas, media_progresso


def filtrar_dados(df, semanas, turmas, cursos, info_contato):
    
    """ Filtra os dados de progresso com base nas semanas, turmas e cursos selecionados. """
    
    semana_inicial, semana_final = semanas
    df_filtered = df[df['semana_ano'].between(semana_inicial, semana_final)]
    df_filtered = df_filtered[df_filtered['turma'].isin(turmas)]

    colunas_selecionadas = ['aluno_email', 'nome', 'celular', 'semana_ano', 'turma'] if info_contato else ['aluno_email', 'semana_ano', 'turma']
    colunas_selecionadas.extend(cursos)

    return df_filtered[colunas_selecionadas]


def get_semanas(df):

    """ Retorna a última semana e a semana anterior. """

    ultima_semana = df['semana_ano'].max()
    semanas_ordenadas = np.sort(df['semana_ano'].unique())
    
    if len(semanas_ordenadas) < 2:
        semana_anterior = ultima_semana
    else:
        semana_anterior = semanas_ordenadas[-2]
    

    return ultima_semana, semana_anterior

def filtrar_semanas(df, semana):
    
    """ Filtra os dados com base na semana selecionada. """

    return df[df['semana_ano'] == semana]

def calcular_deltas(valores_ultima, valores_anterior):
    
    """ Calcula a diferença entre os valores da última semana e da semana anterior. """
    
    return valores_ultima - valores_anterior

def exportar_para_excel(df):
        
    """ Função para exportar um DataFrame para um arquivo Excel e disponibilizar um link para download. """

    towrite = io.BytesIO()
    df.to_excel(towrite, index=True, sheet_name='Sheet1')  # index=True para incluir o índice
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="progresso_alunos.xlsx">Download Excel</a>'
    
    st.markdown(href, unsafe_allow_html=True)
