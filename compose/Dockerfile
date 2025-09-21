FROM python:3.11-alpine

# Diretório de trabalho
WORKDIR /app

# Dependências de sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY api/ .
COPY app/ ./app/

# Criar diretório de logs
RUN mkdir -p /app/logs

# Usuário não-root (Alpine)
RUN addgroup -S app \
    && adduser -S -G app app \
    && chown -R app:app /app
USER app

ENV PYTHONPATH=/app

# Expor porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

