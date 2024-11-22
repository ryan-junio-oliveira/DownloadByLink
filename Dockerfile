# Usar uma imagem oficial do Python com GUI e suporte a áudio
FROM python:3.9-slim

# Instalar as dependências de sistema
RUN apt-get update && apt-get install -y \
    python3-tk \
    ffmpeg \
    && apt-get clean

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o conteúdo do diretório local para o diretório de trabalho no container
COPY . /app

# Instalar as bibliotecas Python necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar a aplicação
CMD ["python", "app.py"]
