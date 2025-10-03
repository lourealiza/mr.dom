#!/bin/bash

# Script para resetar o PostgreSQL com novas configurações
# Este script remove o volume do PostgreSQL e recria com as novas configurações

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "=========================================="
echo "  Reset do PostgreSQL - MrDom SDR"
echo "=========================================="
echo

# Confirmar ação
echo -n "Tem certeza que deseja resetar o PostgreSQL? Isso irá apagar todos os dados. (y/N): "
read -r response
case "$response" in
    [yY]|[yY][eE][sS])
        echo "Continuando com o reset..."
        ;;
    *)
        echo "Operação cancelada."
        exit 0
        ;;
esac

# Parar containers
log "Parando containers..."
docker-compose -f compose/docker-compose.yml down 2>/dev/null || true
docker-compose -f compose/docker-compose.test.yml down 2>/dev/null || true

# Remover volume do PostgreSQL
log "Removendo volume do PostgreSQL..."
docker volume rm mrdom-postgres_data 2>/dev/null || true

# Remover container do PostgreSQL se existir
log "Removendo container do PostgreSQL..."
docker rm mrdom-postgres 2>/dev/null || true

# Recriar e iniciar PostgreSQL
log "Recriando PostgreSQL com novas configurações..."
docker-compose -f compose/docker-compose.yml up -d postgres

# Aguardar PostgreSQL inicializar
log "Aguardando PostgreSQL inicializar..."
sleep 10

# Verificar se PostgreSQL está rodando
log "Verificando status do PostgreSQL..."
if docker ps | grep -q mrdom-postgres; then
    success "PostgreSQL está rodando!"
else
    error "PostgreSQL não está rodando!"
    exit 1
fi

# Testar conexão
log "Testando conexão com PostgreSQL..."
docker exec mrdom-postgres psql -U app -d app -c "SELECT version();" >/dev/null 2>&1

if [ $? -eq 0 ]; then
    success "Conexão com PostgreSQL bem-sucedida!"
else
    error "Falha na conexão com PostgreSQL!"
    exit 1
fi

echo
echo "=========================================="
success "PostgreSQL resetado com sucesso!"
echo "=========================================="
echo
echo "Nova configuração:"
echo "  Host: postgres (ou localhost)"
echo "  Porta: 5432"
echo "  Database: app"
echo "  Usuário: app"
echo "  Senha: mrdom2024"
echo
echo "Para conectar no N8N ou outras ferramentas:"
echo "  Host: localhost"
echo "  Porta: 5432"
echo "  Database: app"
echo "  Usuário: app"
echo "  Senha: mrdom2024"
echo
