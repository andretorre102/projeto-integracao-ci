# Usa uma imagem oficial do Python, bem leve
FROM python:3.12-slim

# Atualizar os pacotes do sistema operacional Debian para aplicar os patches de segurança, limpando o cache e os arquivos temporários.
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (otimização de cache do Docker)
COPY requirements.txt .

# Atualiza as ferramentas base do python e instala dependências
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \ 
pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação para dentro do container
COPY . .

# Expõe a porta 5000 para o mundo exterior
EXPOSE 5000

# Fazer a aplicação escutar em todas as interfaces dentro do container:
ENV APP_HOST=0.0.0.0

# Comando para rodar a aplicação quando o container iniciar
CMD ["python", "app.py"]
