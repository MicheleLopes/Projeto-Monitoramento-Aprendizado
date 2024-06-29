import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Carregar a configuração de autenticação
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def inicializar_variaveis():
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None

    if 'name' not in st.session_state:
        st.session_state['name'] = None
        
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    if 'logout' not in st.session_state:
        st.session_state.logout = True
    return st.session_state['authentication_status'], st.session_state['name'], st.session_state['username'], st.session_state.logout

def autenticar_usuario():
    #Autenticação do usuário
    name, authentication_status, username = authenticator.login(fields={'Login': 'Login', 'main': 'main'})
    st.session_state['authentication_status'] = authentication_status
    return st.session_state['authentication_status'], name, authentication_status, username
