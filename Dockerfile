FROM python:3.11-slim

# Instala dependências do sistema (Z3 e build tools)
RUN apt-get update && apt-get install -y \
    z3 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia requirements.txt (vamos criar)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Comando padrão
CMD ["python", "solver.py"]
