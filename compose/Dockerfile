FROM python:3.11-alpine

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
# Copiar código da aplicação (API) e pacotes internos
COPY api/ .
COPY app/ ./app/

# Criar diretório para logs
RUN mkdir -p /app/logs

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENV PYTHONPATH=/app

# Expor porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
