import pandas as pd

def get_info_trilha(trilha):
    
    """" Função para retornar as colunas ordenadas e os novos nomes das turmas ."""

    if trilha == 'analista':
        colunas_ordenadas = [91198,106192,106193,122093,171026,90700,100834,144463,100840,106200,100836,106202,106203,172226]
        cols_new = {
            91198: 'boas_vindas',
            106192: 'portifolio',
            106193: 'linkedin',
            122093: 'SQL',
            171026: 'metricas_negocio',
            90700:  'excel',
            100834: 'power_bi',
            144463: 'estatistica',
            100840: 'ad_producao',
            106200: 'storytelling',
            100836: 'bd_relacional',
            106202: 'recrutamento_rh',
            106203: 'FTC',
            172226: 'ETL'
        }
    elif trilha == 'cientista':
        colunas_ordenadas = [91197,90693,90695,90729,90730,90731,91224,91214,91217,91222,162188,91223,90726,91226,168903,91228,91230,91232,91233]
        cols_new = {
        91197: 'boas_vindas',
        90693: 'portifolio',
        90695: 'linkedin',
        90729: 'FTC',
        90730: 'SQL',
        90731:  'GIT',
        91224: 'ambiente_virtual',
        91214: 'fundamentos_ML',
        91217: 'DS_producao',
        91222: 'storytelling',
        162188: 'estatistica',
        91223: 'PA_classificao',
        90726: 'metricas_negocio',
        91226: 'PA_clusterizacao',
        168903: 'BD_relacional',
        91228: 'RH',
        91230: 'elasticidade_preco',
        91232: 'GCP',
        91233: 'AWS'
        }
    else:
        raise ValueError(f"Trilha desconhecida: {trilha}")

    return colunas_ordenadas, cols_new

def data_clean(df, trilha):

    """" Função para limpar os dados e retornar a tabela pivotada com as colunas ordenadas e renomeadas """
    

    colunas_ordenadas, cols_new = get_info_trilha(trilha)

    # substituir null por da coluna celular por Nao informado
    df['celular'] = df['celular'].fillna('Não informado')

    # pivotando a tabela
    df_pivot = df.pivot_table(index=['aluno_email','nome','celular','semana_ano','turma'], columns=['produto_id'], values='progresso_do_aluno', aggfunc='first')   
    
    # Reordenando as colunas e resetando o índice
    df_final = df_pivot[colunas_ordenadas].reset_index().rename_axis(None, axis=1)

    # renomear colunas
    df_final.rename(columns=cols_new, inplace=True)
    
    # retirar % dos valores
    df_final = df_final.replace('%', '', regex=True)

    df_final.fillna(0, inplace=True)

    
    return df_final


def formatar_valor(val):
    # Verifica se o valor é numérico e retorna uma string formatada
    if isinstance(val, (int, float)):
        return "{:.2f}".format(val)
    return val

def visao_semana(df):
    # Lista de colunas dos cursos
    colunas_cursos = [col for col in df.columns if col not in ['aluno_email', 'nome', 'celular', 'turma', 'semana_ano']]

    # média geral dos cursos para cada 'turma' e 'semana_ano'
    df['Progresso'] = df[colunas_cursos].mean(axis=1)

    # Agrupar por 'turma' e 'semana_ano', calcular a média de 'Progresso' e contar o número de 'aluno_email'
    tabela = df.groupby(['turma', 'semana_ano']).agg({'Progresso': 'mean', 'aluno_email': 'nunique'})

    # Renomear as colunas
    tabela.rename(columns={'aluno_email': 'QTD'}, inplace=True)

    # Arredondar e alterar o tipo de dados
    tabela['Progresso'] = tabela['Progresso'].round(2)
    tabela['QTD'] = tabela['QTD'].astype(int)

    # Remodelar a tabela para que 'Progresso' e 'QTD' estejam aninhados sob cada 'semana_ano'
    tabela_pivot = tabela.unstack().swaplevel(0, 1, axis=1).sort_index(axis=1)

    # Converter todas as linhas em strings formatadas corretamente
    tabela_pivot = tabela_pivot.map(formatar_valor)

    # Remover ".00" de 'QTD' e substituir 'nan' por '0'
    tabela_pivot = tabela_pivot.replace('\.00', '', regex=True).replace('nan', '0')

    return tabela_pivot