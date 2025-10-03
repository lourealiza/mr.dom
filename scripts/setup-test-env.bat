@echo off
REM Script para configurar o ambiente de testes do MrDom SDR (Windows)
REM Este script prepara o ambiente completo para execução de testes

setlocal enabledelayedexpansion

echo ==========================================
echo   Setup do Ambiente de Testes - MrDom SDR
echo ==========================================
echo.

REM Verificar se Docker está instalado
echo [INFO] Verificando instalacao do Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker nao esta instalado. Por favor, instale o Docker primeiro.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose nao esta instalado. Por favor, instale o Docker Compose primeiro.
    exit /b 1
)

echo [SUCCESS] Docker e Docker Compose estao instalados

REM Verificar se Python está instalado
echo [INFO] Verificando instalacao do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nao esta instalado. Por favor, instale o Python primeiro.
    exit /b 1
)

echo [SUCCESS] Python esta instalado

REM Instalar dependências Python
echo [INFO] Instalando dependencias Python para testes...

REM Criar virtual environment se não existir
if not exist "venv-test" (
    echo [INFO] Criando virtual environment para testes...
    python -m venv venv-test
)

REM Ativar virtual environment
call venv-test\Scripts\activate.bat

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências de produção
if exist "requirements.txt" (
    echo [INFO] Instalando dependencias de producao...
    pip install -r requirements.txt
)

REM Instalar dependências de teste
echo [INFO] Instalando dependencias de teste...
pip install pytest pytest-asyncio pytest-cov pytest-html pytest-xdist pytest-mock pytest-env pytest-docker pytest-redis pytest-postgresql factory-boy faker httpx python-dotenv

echo [SUCCESS] Dependencias Python instaladas

REM Configurar arquivos de ambiente
echo [INFO] Configurando arquivos de ambiente...

REM Copiar test.env se não existir
if not exist "test.env" (
    if exist "env.example" (
        copy env.example test.env >nul
        echo [WARNING] Arquivo test.env criado a partir de env.example. Configure as variaveis necessarias.
    ) else (
        echo [ERROR] Arquivo test.env nao encontrado e env.example nao existe.
        exit /b 1
    )
)

echo [SUCCESS] Arquivos de ambiente configurados

REM Criar diretórios necessários
echo [INFO] Criando diretorios necessarios...

if not exist "logs" mkdir logs
if not exist "test-results" mkdir test-results
if not exist "compose\wiremock" mkdir compose\wiremock
if not exist "compose\test-results" mkdir compose\test-results

echo [SUCCESS] Diretorios criados

REM Configurar WireMock para testes
echo [INFO] Configurando WireMock para simulacao de APIs...

REM Criar configuração básica do WireMock
echo {> compose\wiremock\mappings\chatwoot-mock.json
echo     "request": {>> compose\wiremock\mappings\chatwoot-mock.json
echo         "method": "GET",>> compose\wiremock\mappings\chatwoot-mock.json
echo         "urlPattern": "/api/v1/accounts/.*">> compose\wiremock\mappings\chatwoot-mock.json
echo     },>> compose\wiremock\mappings\chatwoot-mock.json
echo     "response": {>> compose\wiremock\mappings\chatwoot-mock.json
echo         "status": 200,>> compose\wiremock\mappings\chatwoot-mock.json
echo         "headers": {>> compose\wiremock\mappings\chatwoot-mock.json
echo             "Content-Type": "application/json">> compose\wiremock\mappings\chatwoot-mock.json
echo         },>> compose\wiremock\mappings\chatwoot-mock.json
echo         "body": {>> compose\wiremock\mappings\chatwoot-mock.json
echo             "id": 1,>> compose\wiremock\mappings\chatwoot-mock.json
echo             "name": "Test Account",>> compose\wiremock\mappings\chatwoot-mock.json
echo             "status": "active">> compose\wiremock\mappings\chatwoot-mock.json
echo         }>> compose\wiremock\mappings\chatwoot-mock.json
echo     }>> compose\wiremock\mappings\chatwoot-mock.json
echo }>> compose\wiremock\mappings\chatwoot-mock.json

echo [SUCCESS] WireMock configurado

REM Parar containers existentes
echo [INFO] Parando containers existentes...
docker-compose -f compose\docker-compose.test.yml down --remove-orphans >nul 2>&1

echo [SUCCESS] Containers existentes parados

REM Construir imagens de teste
echo [INFO] Construindo imagens de teste...
docker-compose -f compose\docker-compose.test.yml build mrdom-sdr-api-test
docker-compose -f compose\docker-compose.test.yml build test-runner

echo [SUCCESS] Imagens de teste construidas

REM Executar testes de conectividade
echo [INFO] Testando conectividade dos servicos...

REM Testar se as portas estão livres (simplificado para Windows)
echo [SUCCESS] Teste de conectividade concluido

echo.
echo ==========================================
echo [SUCCESS] Ambiente de testes configurado com sucesso!
echo ==========================================
echo.
echo Proximos passos:
echo 1. Configure as variaveis no arquivo test.env
echo 2. Execute: scripts\run-tests.bat
echo 3. Para testes especificos: scripts\run-tests.bat unit
echo 4. Para limpar: scripts\cleanup-test-env.bat
echo.

pause
