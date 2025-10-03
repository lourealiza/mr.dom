#!/bin/bash

# Script para executar testes do MrDom SDR
# Este script permite executar diferentes tipos de testes

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

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [TIPO] [OPÇÕES]"
    echo
    echo "Tipos de teste disponíveis:"
    echo "  unit        - Testes unitários (padrão)"
    echo "  integration - Testes de integração"
    echo "  e2e         - Testes end-to-end"
    echo "  all         - Todos os testes"
    echo "  coverage    - Testes com relatório de cobertura"
    echo "  docker      - Executar testes em containers Docker"
    echo
    echo "Opções:"
    echo "  --verbose   - Modo verboso"
    echo "  --parallel  - Executar testes em paralelo"
    echo "  --no-cov    - Sem relatório de cobertura"
    echo "  --help      - Mostrar esta ajuda"
    echo
    echo "Exemplos:"
    echo "  $0                    # Executar testes unitários"
    echo "  $0 integration        # Executar testes de integração"
    echo "  $0 all --parallel     # Executar todos os testes em paralelo"
    echo "  $0 docker             # Executar testes em Docker"
    echo "  $0 coverage --verbose # Testes com cobertura detalhada"
}

# Função para verificar dependências
check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar se pytest está instalado
    if ! command -v pytest &> /dev/null; then
        error "pytest não está instalado. Execute: pip install pytest"
        exit 1
    fi
    
    # Verificar se o arquivo test.env existe
    if [ ! -f "test.env" ]; then
        warning "Arquivo test.env não encontrado. Usando configurações padrão."
    fi
    
    success "Dependências verificadas"
}

# Função para configurar ambiente
setup_environment() {
    log "Configurando ambiente de teste..."
    
    # Carregar variáveis de ambiente de teste
    if [ -f "test.env" ]; then
        source test.env
        log "Variáveis de ambiente carregadas de test.env"
    fi
    
    # Criar diretórios necessários
    mkdir -p test-results
    mkdir -p htmlcov
    
    # Definir variáveis de ambiente para pytest
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    export TESTING=true
    
    success "Ambiente configurado"
}

# Função para executar testes unitários
run_unit_tests() {
    log "Executando testes unitários..."
    
    local pytest_args="-m unit --tb=short"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -v"
    fi
    
    if [ "$PARALLEL" = true ]; then
        pytest_args="$pytest_args -n auto"
    fi
    
    if [ "$NO_COV" = false ]; then
        pytest_args="$pytest_args --cov=api --cov-report=term-missing"
    fi
    
    pytest $pytest_args api/tests/
    
    success "Testes unitários concluídos"
}

# Função para executar testes de integração
run_integration_tests() {
    log "Executando testes de integração..."
    
    local pytest_args="-m integration --tb=short --timeout=30"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -v"
    fi
    
    pytest $pytest_args api/tests/
    
    success "Testes de integração concluídos"
}

# Função para executar testes e2e
run_e2e_tests() {
    log "Executando testes end-to-end..."
    
    local pytest_args="-m e2e --tb=short --timeout=60"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -v"
    fi
    
    pytest $pytest_args api/tests/
    
    success "Testes end-to-end concluídos"
}

# Função para executar todos os testes
run_all_tests() {
    log "Executando todos os testes..."
    
    local pytest_args="--tb=short"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -v"
    fi
    
    if [ "$PARALLEL" = true ]; then
        pytest_args="$pytest_args -n auto"
    fi
    
    if [ "$NO_COV" = false ]; then
        pytest_args="$pytest_args --cov=api --cov-report=html:htmlcov --cov-report=term-missing --cov-report=xml"
    fi
    
    pytest $pytest_args api/tests/
    
    success "Todos os testes concluídos"
}

# Função para executar testes com cobertura
run_coverage_tests() {
    log "Executando testes com relatório de cobertura..."
    
    local pytest_args="--cov=api --cov-report=html:htmlcov --cov-report=term-missing --cov-report=xml --cov-fail-under=80"
    
    if [ "$VERBOSE" = true ]; then
        pytest_args="$pytest_args -v"
    fi
    
    pytest $pytest_args api/tests/
    
    success "Relatório de cobertura gerado em htmlcov/index.html"
}

# Função para executar testes em Docker
run_docker_tests() {
    log "Executando testes em containers Docker..."
    
    # Verificar se Docker está rodando
    if ! docker info &> /dev/null; then
        error "Docker não está rodando. Inicie o Docker primeiro."
        exit 1
    fi
    
    # Parar containers existentes
    docker-compose -f compose/docker-compose.test.yml down --remove-orphans 2>/dev/null || true
    
    # Construir e executar testes
    docker-compose -f compose/docker-compose.test.yml up --build --abort-on-container-exit test-runner
    
    # Copiar resultados para o host
    docker cp mrdom-test-runner:/app/test-results ./test-results/ 2>/dev/null || true
    
    success "Testes em Docker concluídos"
}

# Função para limpar após os testes
cleanup() {
    log "Limpando arquivos temporários..."
    
    # Remover arquivos .pyc
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Remover arquivos de cache do pytest
    rm -rf .pytest_cache 2>/dev/null || true
    
    success "Limpeza concluída"
}

# Função para mostrar resultados
show_results() {
    echo
    echo "=========================================="
    echo "  Resultados dos Testes - MrDom SDR"
    echo "=========================================="
    
    if [ -f "test-results/junit.xml" ]; then
        echo "Relatório JUnit: test-results/junit.xml"
    fi
    
    if [ -f "test-results/report.html" ]; then
        echo "Relatório HTML: test-results/report.html"
    fi
    
    if [ -d "htmlcov" ]; then
        echo "Relatório de Cobertura: htmlcov/index.html"
    fi
    
    if [ -f "test-results/pytest.log" ]; then
        echo "Log detalhado: test-results/pytest.log"
    fi
    
    echo "=========================================="
}

# Processar argumentos
TEST_TYPE="unit"
VERBOSE=false
PARALLEL=false
NO_COV=false

while [[ $# -gt 0 ]]; do
    case $1 in
        unit|integration|e2e|all|coverage|docker)
            TEST_TYPE="$1"
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --no-cov)
            NO_COV=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            error "Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Função principal
main() {
    echo "=========================================="
    echo "  Executando Testes - MrDom SDR"
    echo "=========================================="
    echo "Tipo: $TEST_TYPE"
    echo "Verbose: $VERBOSE"
    echo "Paralelo: $PARALLEL"
    echo "Sem cobertura: $NO_COV"
    echo "=========================================="
    echo
    
    check_dependencies
    setup_environment
    
    # Executar testes baseado no tipo
    case $TEST_TYPE in
        unit)
            run_unit_tests
            ;;
        integration)
            run_integration_tests
            ;;
        e2e)
            run_e2e_tests
            ;;
        all)
            run_all_tests
            ;;
        coverage)
            run_coverage_tests
            ;;
        docker)
            run_docker_tests
            ;;
        *)
            error "Tipo de teste inválido: $TEST_TYPE"
            show_help
            exit 1
            ;;
    esac
    
    cleanup
    show_results
    
    echo
    success "Testes executados com sucesso!"
}

# Executar função principal
main "$@"
