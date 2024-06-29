#libraries
import streamlit as st
from PIL import Image
import sys
sys.path.append("..")
from auth.auth import autenticar_usuario, inicializar_variaveis
from functions import streamlit_functions


favicon = Image.open('img/logo_ds.png')
st.set_page_config(page_title='Inserir nova tag', page_icon=favicon)


# ====================================================================
#                Inicio da estratura lógica do codigo
# ====================================================================

def main():
    
    st.session_state['authentication_status'], st.session_state['name'], st.session_state['username'], st.session_state.logout=inicializar_variaveis()
    st.session_state['authentication_status'], name, authentication_status, username = autenticar_usuario()

    if st.session_state['authentication_status']:
      
        st.title("Inserir nova tag")
        st.header("", divider='rainbow')
        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)

        # Solicitar ao usuário para inserir uma nova tag e o número da turma correspondente
        nova_tag = st.text_input("Digite o número da nova tag: ")
        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        numero_turma = st.text_input("Digite o número da turma que ela corresponde: ")
        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        nome_trilha = st.selectbox('Selecione qual trilha pertence essa tag', ['cientista', 'analista'])
        st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        adicionar = st.button("Incluir turma na lista de automação")
        streamlit_functions.processar_inputs(nova_tag, numero_turma, adicionar,nome_trilha)
    
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    
    elif authentication_status == None:
        st.warning('Please enter your username and password') 


if __name__ == "__main__":
    main()