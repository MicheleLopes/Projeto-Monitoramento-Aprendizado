# IMPORTS
import streamlit as st
from PIL import Image
import pandas as pd
from auth.auth import autenticar_usuario, inicializar_variaveis
from functions import streamlit_functions, bigquery_client, data_processing

# ====================================================================
#                             Page congig
# ====================================================================

favicon = Image.open('img/logo_ds.png')
st.set_page_config(page_title='Progresso Turmas Analista', page_icon=favicon)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


# ====================================================================
#                Inicio da estrutura lógica do codigo
# ====================================================================

# Função principal com autenticação
def main():
    
    st.session_state['authentication_status'], st.session_state['name'], st.session_state['username'], st.session_state.logout=inicializar_variaveis()
    st.session_state['authentication_status'], name, authentication_status, username = autenticar_usuario()

    if st.session_state['authentication_status']:
        
        # Carregar e tratar os dados
        df = bigquery_client.carregar_dados('analista')

        # ====================================================================
        #                            Barra lateral
        # ====================================================================
        with st.sidebar.container() as sidebar_image_container:
            st.image("img/logo_ds3.png", use_column_width=True, output_format='PNG')
            st.sidebar.markdown('---')

        st.sidebar.markdown('## Personalize abaixo sua visualização:')
        
        # Obter a primeira e a última semana do dataset
        min_semana = df['semana_ano'].min()
        max_semana = df['semana_ano'].max()

        # Usar min_semana e max_semana como os valores mínimo e máximo para o slider
        semanas = st.sidebar.slider('Semanas que gostaria de visualizar:', min_value=min_semana, max_value=max_semana, value=(min_semana, max_semana))
        st.sidebar.markdown('---')
        
        # Extrair valores únicos da coluna 'turma'
        valores_unicos_turma = df['turma'].unique().tolist()

        turmas = st.sidebar.multiselect("Selecione as turmas que gostaria de visualizar:", valores_unicos_turma, 
                                        default=valores_unicos_turma)
        st.sidebar.markdown('---')
        cursos = st.sidebar.multiselect("Selecione os cursos que gostaria de visualizar:",
                                        ['boas_vindas', 'portifolio', 'linkedin', 'SQL', 'metricas_negocio', 'excel', 
                                        'power_bi', 'estatistica', 'ad_producao', 'storytelling', 'bd_relacional', 
                                        'recrutamento_rh', 'FTC', 'ETL'], default=['boas_vindas', 'portifolio', 'linkedin',
                                        'SQL', 'metricas_negocio', 'excel','power_bi', 'estatistica', 'ad_producao', 'storytelling',
                                        'bd_relacional','recrutamento_rh', 'FTC', 'ETL'])
        st.sidebar.markdown('---')
        
        info_contato = st.sidebar.checkbox('Selecione para visualizar dados de contato (e-mail e telefone)', value=True)

        # Filtrar os dados com base nas seleções do usuário
        df = streamlit_functions.filtrar_dados(df, semanas, turmas, cursos, info_contato)
        

        #  ====================================================================
        #                           Layout no Streamlit
        #  ====================================================================

        
        #  ============================== KPI =================================
        # Titulo e cabeçalho
        st.title("Progresso dos Alunos")
        st.header("", divider='rainbow')
        
        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)

        # Uso das funções
        ultima_semana, semana_anterior = streamlit_functions.get_semanas(df)

        if ultima_semana and semana_anterior:
            df_ultima_semana = streamlit_functions.filtrar_semanas(df, ultima_semana)
            df_semana_anterior = streamlit_functions.filtrar_semanas(df, semana_anterior)

            total_alunos_ultima, total_turmas_ultima, media_progresso_ultima = streamlit_functions.calcular_kpis(df_ultima_semana, cursos)
            total_alunos_anterior, total_turmas_anterior, media_progresso_anterior = streamlit_functions.calcular_kpis(df_semana_anterior, cursos)

            delta_alunos = streamlit_functions.calcular_deltas(total_alunos_ultima, total_alunos_anterior)
            delta_turmas = streamlit_functions.calcular_deltas(total_turmas_ultima, total_turmas_anterior)
            delta_progresso = streamlit_functions.calcular_deltas(media_progresso_ultima, media_progresso_anterior)


        # Criação dos cards com as métricas
        col1, col2, col3 = st.columns(3)

        # Card 1: Total de Alunos
        col1.metric("Total de Alunos", total_alunos_ultima, delta=delta_alunos)

        # Card 2: Total de Turmas
        col2.metric("Total de Turmas", total_turmas_ultima, delta=delta_turmas)

        # Card 3: Média de Progresso
        col3.metric("Média de Progresso", f"{media_progresso_ultima:.2f}%", delta=f"{delta_progresso:.2f}%")
        
        st.header("", divider='rainbow')

        #================================Tabela===================================

        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        # Widget de seleção para escolher entre visão geral e visão por turma
        visao = st.selectbox('Escolha a visão:', ('','Geral', 'Por Turma'))

        if visao:

            if visao == 'Geral':
                with st.container():
                    
                    # Widget de entrada de texto para busca
                    busca = st.text_input("Digite um e-mail específico para busca:")
                    
                    # Filtrando os dados com base no e-mail
                    if busca:
                        if 'aluno_email' in df.columns:
                            resultados = df[df['aluno_email'].str.contains(busca)]
                        else:
                            resultados = pd.DataFrame(columns=df.columns)
                    else:
                        resultados = df
                    df = resultados

                    st.markdown('### Visualize na tabela abaixo o progresso dos alunos:')
                    st.dataframe(df)

                    # Donwload button
                    if st.button('Exportar para Excel'):
                        streamlit_functions.exportar_para_excel(df)
            
            elif visao == 'Por Turma':
                with st.container():
                    df = data_processing.visao_semana(df)

                    st.markdown('### Visualize na tabela abaixo o progresso das turmas:')
                    st.dataframe(df)

                    # Para usar a função, substitua a parte relevante no botão de download por:
                    if st.button('Exportar para Excel'):
                        streamlit_functions.exportar_para_excel(df)


    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()