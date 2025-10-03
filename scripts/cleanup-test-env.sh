#!/bin/bash

# Script para limpar o ambiente de testes do MrDom SDR
# Este script remove containers, volumes e arquivos temporários de teste

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
    echo "Uso: $0 [OPÇÕES]"
    echo
    echo "Opções:"
    echo "  --containers  - Parar e remover apenas containers de teste"
    echo "  --volumes      - Remover volumes de teste"
    echo "  --images       - Remover imagens de teste"
    echo "  --files        - Remover arquivos temporários"
    echo "  --all          - Limpeza completa (padrão)"
    echo "  --force        - Forçar remoção sem confirmação"
    echo "  --help         - Mostrar esta ajuda"
    echo
    echo "Exemplos:"
    echo "  $0                    # Limpeza completa com confirmação"
    echo "  $0 --containers       # Apenas containers"
    echo "  $0 --all --force     # Limpeza completa sem confirmação"
}

# Função para confirmar ação
confirm_action() {
    if [ "$FORCE" = true ]; then
        return 0
    fi
    
    echo -n "Tem certeza que deseja continuar? (y/N): "
    read -r response
    case "$response" in
        [yY]|[yY][eE][sS])
            return 0
            ;;
        *)
            echo "Operação cancelada."
            exit 0
            ;;
    esac
}

# Função para parar containers de teste
stop_test_containers() {
    log "Parando containers de teste..."
    
    # Parar containers específicos de teste
    containers=(
        "mrdom-sdr-api-test"
        "mrdom-redis-test"
        "mrdom-postgres"
        "mrdom-n8n-test"
        "mrdom-mock-server"
        "mrdom-test-runner"
    )
    
    for container in "${containers[@]}"; do
        if docker ps -q -f name="$container" | grep -q .; then
            log "Parando container: $container"
            docker stop "$container" 2>/dev/null || true
        fi
    done
    
    # Parar todos os containers do docker-compose de teste
    docker-compose -f compose/docker-compose.test.yml down --remove-orphans 2>/dev/null || true
    
    success "Containers de teste parados"
}

# Função para remover containers de teste
remove_test_containers() {
    log "Removendo containers de teste..."
    
    # Remover containers específicos de teste
    containers=(
        "mrdom-sdr-api-test"
        "mrdom-redis-test"
        "mrdom-postgres"
        "mrdom-n8n-test"
        "mrdom-mock-server"
        "mrdom-test-runner"
    )
    
    for container in "${containers[@]}"; do
        if docker ps -aq -f name="$container" | grep -q .; then
            log "Removendo container: $container"
            docker rm "$container" 2>/dev/null || true
        fi
    done
    
    success "Containers de teste removidos"
}

# Função para remover volumes de teste
remove_test_volumes() {
    log "Removendo volumes de teste..."
    
    # Remover volumes específicos de teste
    volumes=(
        "mrdom-redis_test_data"
        "mrdom-postgres_data"
        "mrdom-n8n_test_data"
    )
    
    for volume in "${volumes[@]}"; do
        if docker volume ls -q | grep -q "^${volume}$"; then
            log "Removendo volume: $volume"
            docker volume rm "$volume" 2>/dev/null || true
        fi
    done
    
    success "Volumes de teste removidos"
}

# Função para remover imagens de teste
remove_test_images() {
    log "Removendo imagens de teste..."
    
    # Remover imagens específicas de teste
    images=(
        "mrdom-sdr-api-test"
        "mrdom-test-runner"
    )
    
    for image in "${images[@]}"; do
        if docker images -q "$image" | grep -q .; then
            log "Removendo imagem: $image"
            docker rmi "$image" 2>/dev/null || true
        fi
    done
    
    # Remover imagens órfãs
    log "Removendo imagens órfãs..."
    docker image prune -f 2>/dev/null || true
    
    success "Imagens de teste removidas"
}

# Função para remover arquivos temporários
remove_temp_files() {
    log "Removendo arquivos temporários..."
    
    # Diretórios e arquivos para remover
    items_to_remove=(
        "test-results"
        "htmlcov"
        ".pytest_cache"
        "venv-test"
        "*.pyc"
        "__pycache__"
        ".coverage"
        "coverage.xml"
        ".mypy_cache"
        ".tox"
        "dist"
        "build"
        "*.egg-info"
    )
    
    for item in "${items_to_remove[@]}"; do
        if [ -e "$item" ] || [ -d "$item" ]; then
            log "Removendo: $item"
            rm -rf "$item" 2>/dev/null || true
        fi
    done
    
    # Remover arquivos .pyc recursivamente
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    success "Arquivos temporários removidos"
}

# Função para limpar logs
cleanup_logs() {
    log "Limpando logs de teste..."
    
    if [ -d "logs" ]; then
        log "Removendo logs antigos..."
        find logs -name "*.log" -mtime +7 -delete 2>/dev/null || true
        find logs -name "test-*" -delete 2>/dev/null || true
    fi
    
    success "Logs limpos"
}

# Função para mostrar estatísticas
show_stats() {
    echo
    echo "=========================================="
    echo "  Estatísticas de Limpeza"
    echo "=========================================="
    
    # Contar containers
    container_count=$(docker ps -aq | wc -l)
    echo "Containers restantes: $container_count"
    
    # Contar volumes
    volume_count=$(docker volume ls -q | wc -l)
    echo "Volumes restantes: $volume_count"
    
    # Contar imagens
    image_count=$(docker images -q | wc -l)
    echo "Imagens restantes: $image_count"
    
    # Espaço em disco liberado
    if command -v du &> /dev/null; then
        disk_usage=$(du -sh . 2>/dev/null | cut -f1)
        echo "Uso de disco atual: $disk_usage"
    fi
    
    echo "=========================================="
}

# Processar argumentos
CLEAN_CONTAINERS=false
CLEAN_VOLUMES=false
CLEAN_IMAGES=false
CLEAN_FILES=false
CLEAN_ALL=true
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --containers)
            CLEAN_CONTAINERS=true
            CLEAN_ALL=false
            shift
            ;;
        --volumes)
            CLEAN_VOLUMES=true
            CLEAN_ALL=false
            shift
            ;;
        --images)
            CLEAN_IMAGES=true
            CLEAN_ALL=false
            shift
            ;;
        --files)
            CLEAN_FILES=true
            CLEAN_ALL=false
            shift
            ;;
        --all)
            CLEAN_ALL=true
            shift
            ;;
        --force)
            FORCE=true
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
    echo "  Limpeza do Ambiente de Testes"
    echo "=========================================="
    echo "Containers: $([ "$CLEAN_CONTAINERS" = true ] || [ "$CLEAN_ALL" = true ] && echo "Sim" || echo "Não")"
    echo "Volumes: $([ "$CLEAN_VOLUMES" = true ] || [ "$CLEAN_ALL" = true ] && echo "Sim" || echo "Não")"
    echo "Imagens: $([ "$CLEAN_IMAGES" = true ] || [ "$CLEAN_ALL" = true ] && echo "Sim" || echo "Não")"
    echo "Arquivos: $([ "$CLEAN_FILES" = true ] || [ "$CLEAN_ALL" = true ] && echo "Sim" || echo "Não")"
    echo "Forçar: $([ "$FORCE" = true ] && echo "Sim" || echo "Não")"
    echo "=========================================="
    echo
    
    # Confirmar ação se não for forçada
    if [ "$FORCE" = false ]; then
        confirm_action
    fi
    
    # Executar limpeza baseada nas opções
    if [ "$CLEAN_ALL" = true ] || [ "$CLEAN_CONTAINERS" = true ]; then
        stop_test_containers
        remove_test_containers
    fi
    
    if [ "$CLEAN_ALL" = true ] || [ "$CLEAN_VOLUMES" = true ]; then
        remove_test_volumes
    fi
    
    if [ "$CLEAN_ALL" = true ] || [ "$CLEAN_IMAGES" = true ]; then
        remove_test_images
    fi
    
    if [ "$CLEAN_ALL" = true ] || [ "$CLEAN_FILES" = true ]; then
        remove_temp_files
        cleanup_logs
    fi
    
    show_stats
    
    echo
    success "Limpeza concluída com sucesso!"
}

# Executar função principal
main "$@"
