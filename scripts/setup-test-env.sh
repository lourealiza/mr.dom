#!/bin/bash

# Script para configurar o ambiente de testes
# Este script prepara o ambiente completo para execução de testes

set -e  # Parar em caso de erro

echo "🚀 Configurando ambiente de testes do MrDom SDR..."

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

# Verificar se Docker está instalado
check_docker() {
    log "Verificando instalação do Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    success "Docker e Docker Compose estão instalados"
}

# Verificar se Python está instalado
check_python() {
    log "Verificando instalação do Python..."
    if ! command -v python3 &> /dev/null; then
        error "Python 3 não está instalado. Por favor, instale o Python 3 primeiro."
        exit 1
    fi
    
    # Verificar versão do Python
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
        error "Python 3.8+ é necessário. Versão atual: $python_version"
        exit 1
    fi
    
    success "Python $python_version está instalado"
}

# Instalar dependências Python
install_python_deps() {
    log "Instalando dependências Python para testes..."
    
    # Criar virtual environment se não existir
    if [ ! -d "venv-test" ]; then
        log "Criando virtual environment para testes..."
        python3 -m venv venv-test
    fi
    
    # Ativar virtual environment
    source venv-test/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências de produção
    if [ -f "requirements.txt" ]; then
        log "Instalando dependências de produção..."
        pip install -r requirements.txt
    fi
    
    # Instalar dependências de teste
    log "Instalando dependências de teste..."
    pip install pytest pytest-asyncio pytest-cov pytest-html pytest-xdist \
                pytest-mock pytest-env pytest-docker pytest-redis \
                pytest-postgresql factory-boy faker httpx python-dotenv
    
    success "Dependências Python instaladas"
}

# Configurar arquivos de ambiente
setup_env_files() {
    log "Configurando arquivos de ambiente..."
    
    # Copiar test.env se não existir
    if [ ! -f "test.env" ]; then
        if [ -f "env.example" ]; then
            cp env.example test.env
            warning "Arquivo test.env criado a partir de env.example. Configure as variáveis necessárias."
        else
            error "Arquivo test.env não encontrado e env.example não existe."
            exit 1
        fi
    fi
    
    # Verificar se as variáveis essenciais estão configuradas
    source test.env
    
    required_vars=("CHATWOOT_BASE_URL" "N8N_BASE_URL" "OPENAI_API_KEY")
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        warning "Variáveis de ambiente não configuradas: ${missing_vars[*]}"
        warning "Configure essas variáveis no arquivo test.env antes de executar os testes"
    fi
    
    success "Arquivos de ambiente configurados"
}

# Criar diretórios necessários
create_directories() {
    log "Criando diretórios necessários..."
    
    directories=(
        "logs"
        "test-results"
        "compose/wiremock"
        "compose/test-results"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log "Diretório criado: $dir"
        fi
    done
    
    success "Diretórios criados"
}

# Configurar WireMock para testes
setup_wiremock() {
    log "Configurando WireMock para simulação de APIs..."
    
    # Criar configuração básica do WireMock
    cat > compose/wiremock/mappings/chatwoot-mock.json << EOF
{
    "request": {
        "method": "GET",
        "urlPattern": "/api/v1/accounts/.*"
    },
    "response": {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "id": 1,
            "name": "Test Account",
            "status": "active"
        }
    }
}
EOF

    cat > compose/wiremock/mappings/n8n-mock.json << EOF
{
    "request": {
        "method": "POST",
        "urlPattern": "/api/v1/workflows/.*/execute"
    },
    "response": {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "execution_id": "test-exec-123",
            "status": "success"
        }
    }
}
EOF

    success "WireMock configurado"
}

# Parar containers existentes
stop_existing_containers() {
    log "Parando containers existentes..."
    
    # Parar containers de teste se estiverem rodando
    docker-compose -f compose/docker-compose.test.yml down --remove-orphans 2>/dev/null || true
    
    success "Containers existentes parados"
}

# Construir imagens de teste
build_test_images() {
    log "Construindo imagens de teste..."
    
    # Construir imagem principal de teste
    docker-compose -f compose/docker-compose.test.yml build mrdom-sdr-api-test
    
    # Construir imagem do test runner
    docker-compose -f compose/docker-compose.test.yml build test-runner
    
    success "Imagens de teste construídas"
}

# Executar testes de conectividade
test_connectivity() {
    log "Testando conectividade dos serviços..."
    
    # Testar se as portas estão livres
    ports=(8001 6380 5433 5679 8080)
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            warning "Porta $port está em uso. Alguns testes podem falhar."
        fi
    done
    
    success "Teste de conectividade concluído"
}

# Função principal
main() {
    echo "=========================================="
    echo "  Setup do Ambiente de Testes - MrDom SDR"
    echo "=========================================="
    echo
    
    check_docker
    check_python
    install_python_deps
    setup_env_files
    create_directories
    setup_wiremock
    stop_existing_containers
    build_test_images
    test_connectivity
    
    echo
    echo "=========================================="
    success "Ambiente de testes configurado com sucesso!"
    echo "=========================================="
    echo
    echo "Próximos passos:"
    echo "1. Configure as variáveis no arquivo test.env"
    echo "2. Execute: ./scripts/run-tests.sh"
    echo "3. Para testes específicos: ./scripts/run-tests.sh unit"
    echo "4. Para limpar: ./scripts/cleanup-test-env.sh"
    echo
}

# Executar função principal
main "$@"

