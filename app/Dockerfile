# Use a imagem base oficial do Python
FROM python:3.10.12

# Defina o diretório de trabalho
WORKDIR /app

# Instale o virtualenv
RUN pip install virtualenv

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN virtualenv venv && . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo
COPY . .

# Defina a variável de ambiente no contêiner
ENV GOOGLE_APPLICATION_CREDENTIALS="credenciais.json"

# Exponha a porta usada pelo Streamlit
EXPOSE 8080

# Comando para iniciar o Streamlit
CMD ["./venv/bin/streamlit", "run", "home.py", "--server.port=8080", "--server.enableCORS=false"]
