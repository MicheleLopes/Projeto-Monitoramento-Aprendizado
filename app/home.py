import streamlit as st
from PIL import Image
from auth.auth import authenticator, inicializar_variaveis, autenticar_usuario

 
favicon = Image.open('img/logo_ds.png')
st.set_page_config(page_title='Home', page_icon=favicon)

st.image("img/logo_ds4.png", use_column_width=True, output_format='PNG')

authentication_status, name, username, st.session_state.logout=inicializar_variaveis()
st.session_state['authentication_status'], name, authentication_status, username = autenticar_usuario()

if st.session_state['authentication_status']:

    st.write("# Seja bem vindo👋")

    st.markdown(
        """
        Esse é o painel para acompanhamento do progresso dos alunos das turmas de analista e cientista de dados.
        
        ### O que você consegue fazer por aqui?

        #### Página Progresso Alunos

        - Acompanhar progresso semanal dos alunos;
        - Usar filtros para personalizar e facilitar a visualização;
        - Exportar planilha com os dados em Excel.

        #### Página Inserir Nova TAG

        - Assim que criada uma nova turma na Cademi, você pode adicioná-la por meio desta página para que 
        entre nas próximas coletas automaticamente.  

    """
    )

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')